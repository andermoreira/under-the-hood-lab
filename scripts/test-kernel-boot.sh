#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${KERNEL_OUT:-$ROOT/build/kernel}"
: "${LIMINE_DIR:?Set LIMINE_DIR to a Limine binary distribution}"
for cmd in xorriso qemu-system-x86_64 timeout; do command -v "$cmd" >/dev/null || { echo "NOT_RUN: missing $cmd" >&2; exit 2; }; done
for file in limine-bios.sys limine-bios-cd.bin limine-uefi-cd.bin; do
  test -f "$LIMINE_DIR/$file" || { echo "NOT_RUN: missing Limine artifact $file" >&2; exit 2; }
done
test -s "$OUT/kernel.elf" || { echo "NOT_RUN: build kernel first" >&2; exit 2; }
mkdir -p "$OUT/iso_root/boot/limine"
cp "$OUT/kernel.elf" "$OUT/iso_root/boot/kernel.elf"
cp "$ROOT/kernel/x86_64/limine.conf" "$OUT/iso_root/boot/limine/limine.conf"
cp "$LIMINE_DIR/limine-bios.sys" "$LIMINE_DIR/limine-bios-cd.bin" "$LIMINE_DIR/limine-uefi-cd.bin" "$OUT/iso_root/boot/limine/"
xorriso -as mkisofs -R -r -J -b boot/limine/limine-bios-cd.bin -no-emul-boot -boot-load-size 4 -boot-info-table --efi-boot boot/limine/limine-uefi-cd.bin -efi-boot-part --efi-boot-image -o "$OUT/kernel.iso" "$OUT/iso_root" >/dev/null 2>&1
"$LIMINE_DIR/limine" bios-install "$OUT/kernel.iso"
rm -f "$OUT/qemu-monitor.sock"
if [[ "${B04_EXPECT_KEYBOARD:-0}" == "1" ]]; then
  python3 - "$OUT/qemu-monitor.sock" "$OUT/serial.log" <<'PY' &
import pathlib, socket, sys, time
sockpath, logpath = sys.argv[1:]
for _ in range(200):
    if pathlib.Path(sockpath).exists() and pathlib.Path(logpath).exists() and "B04_TIMER_TICKS_OK" in pathlib.Path(logpath).read_text(errors="replace"):
        try:
            with socket.socket(socket.AF_UNIX) as sock:
                sock.connect(sockpath)
                sock.settimeout(1)
                sock.recv(4096)
                for command in ("info qtree", "info pic", "sendkey a", "info pic"):
                    sock.sendall((command + "\n").encode())
                    chunks = []
                    deadline = time.monotonic() + 1.5
                    while time.monotonic() < deadline:
                        try:
                            chunk = sock.recv(65536)
                            if not chunk:
                                break
                            chunks.append(chunk)
                        except socket.timeout:
                            break
                    print("QEMU_HMP_" + command.replace(" ", "_") + ":", repr(b"".join(chunks).decode(errors="replace")[-5000:]), flush=True)
            break
        except OSError:
            pass
    time.sleep(.05)
else:
    sys.exit("FAIL: QEMU monitor not ready for keyboard injection")
PY
  injector_pid=$!
fi
set +e
timeout --signal=TERM --kill-after=3s 20s qemu-system-x86_64 -machine q35 -m 128M -cdrom "$OUT/kernel.iso" -boot d -display none -monitor "unix:$OUT/qemu-monitor.sock,server,nowait" -serial "file:$OUT/serial.log" -no-reboot -no-shutdown -d int,cpu_reset -D "$OUT/qemu-debug.log" >"$OUT/qemu.log" 2>&1
rc=$?
set -e
if [[ -n "${injector_pid:-}" ]]; then wait "$injector_pid" || { echo "FAIL: keyboard injection failed" >&2; exit 1; }; fi
if [[ "$rc" != 124 && "$rc" != 0 ]]; then
  echo "FAIL: QEMU exited unexpectedly (status $rc)" >&2
  cat "$OUT/qemu.log" >&2
  exit 1
fi
if ! grep -Fxq 'KERNEL_READY' "$OUT/serial.log"; then
  echo "FAIL: KERNEL_READY not observed on serial console" >&2
  cat "$OUT/serial.log" "$OUT/qemu.log" >&2
  echo '=== First QEMU exception and CPU register snapshot ===' >&2
  python3 - "$OUT/qemu-debug.log" <<'PY' >&2
from pathlib import Path
import sys
lines = Path(sys.argv[1]).read_text(errors="replace").splitlines()
for i, line in enumerate(lines):
    if "check_exception old:" in line or "v=0e" in line:
        print("\\n".join(lines[max(0, i - 8): min(len(lines), i + 55)]))
        break
else:
    print("No CPU exception found in QEMU debug log")
PY
  echo '=== Disassembly around segment transition ===' >&2
  if command -v objdump >/dev/null; then
    objdump -dr "$OUT/interrupts.o" | tail -110 >&2 || true
  fi
  exit 1
fi
if ! grep -Fxq 'B06_KMALLOC_OK' "$OUT/serial.log"; then
  echo 'FAIL: kmalloc size-class, reuse and invalid-free checks not observed' >&2
  cat "$OUT/serial.log" >&2
  exit 1
fi
if ! grep -Fxq 'B06_OWN_PML4_OK' "$OUT/serial.log"; then
  echo 'FAIL: kernel did not switch CR3 to its own PML4' >&2
  cat "$OUT/serial.log" >&2
  exit 1
fi
if ! grep -Fxq 'B06_PAGING_REUSE_OK' "$OUT/serial.log"; then
  echo 'FAIL: repeated paging map/unmap PMM accounting test not observed' >&2
  cat "$OUT/serial.log" >&2
  exit 1
fi
if ! grep -Fxq 'B06_PAGING_ROLLBACK_OK' "$OUT/serial.log"; then
  echo 'FAIL: paging rollback fault-injection checks not observed' >&2
  cat "$OUT/serial.log" >&2
  exit 1
fi
if ! grep -Fxq 'B06_PAGING_MAP_UNMAP_OK' "$OUT/serial.log"; then
  echo 'FAIL: real paging map/unmap smoke test not observed' >&2
  cat "$OUT/serial.log" >&2
  exit 1
fi
if ! grep -Fxq 'B06_HEAP_REUSE_OK' "$OUT/serial.log"; then
  echo 'FAIL: heap zeroing and repeated reuse test not observed' >&2
  cat "$OUT/serial.log" >&2
  exit 1
fi
if ! grep -Fxq 'B06_HEAP_PAGE_OK' "$OUT/serial.log"; then
  echo 'FAIL: page-backed heap smoke test not observed' >&2
  cat "$OUT/serial.log" >&2
  exit 1
fi
if ! grep -Fxq 'B05_PMM_ALLOC_FREE_OK' "$OUT/serial.log"; then
  echo 'FAIL: physical frame allocator smoke test not observed' >&2
  cat "$OUT/serial.log" >&2
  exit 1
fi
if ! grep -Fxq 'B04_TIMER_TICKS_OK' "$OUT/serial.log"; then
  echo 'FAIL: five PIT timer interrupts not observed' >&2
  cat "$OUT/serial.log" >&2
  exit 1
fi
if [[ "${B04_EXPECT_KEYBOARD:-0}" == "1" ]] && ! grep -Fxq "B04_KEYBOARD_IRQ" "$OUT/serial.log"; then
  echo "FAIL: injected PS/2 key did not trigger IRQ1" >&2
  echo "=== Serial evidence ===" >&2
  cat "$OUT/serial.log" >&2
  echo "=== QEMU keyboard IRQ trace ===" >&2
  grep -E "Servicing hardware INT=0x21|v=21|Triple fault|check_exception" "$OUT/qemu-debug.log" | tail -30 >&2 || true
  exit 1
fi
if [[ "${B03_EXPECT_UD2:-0}" == "1" ]]; then
  grep -Fxq 'EXCEPTION_UD_VECTOR_6' "$OUT/serial.log" || { echo 'FAIL: expected #UD missing' >&2; exit 1; }
  python3 - "$OUT/serial.log" <<'PY'
import pathlib, sys
lines = pathlib.Path(sys.argv[1]).read_text().splitlines()
assert lines.index('KERNEL_READY') < lines.index('EXCEPTION_UD_VECTOR_6'), lines
PY
else
  if grep -Fq 'EXCEPTION_UD_VECTOR_6' "$OUT/serial.log"; then echo 'FAIL: unexpected #UD' >&2; exit 1; fi
fi
if [[ "${B06_EXPECT_PF:-0}" == "1" ]]; then
  grep -Fxq 'EXCEPTION_PF_CR2_0x0000000000001000' "$OUT/serial.log" || { echo 'FAIL: expected #PF at lower-half address 0x1000 missing' >&2; cat "$OUT/serial.log" >&2; exit 1; }
  grep -Fxq 'EXCEPTION_PF_ERROR_0x0000000000000000' "$OUT/serial.log" || { echo 'FAIL: expected not-present kernel read error code missing' >&2; cat "$OUT/serial.log" >&2; exit 1; }
else
  if grep -Fq 'EXCEPTION_PF' "$OUT/serial.log"; then echo 'FAIL: unexpected #PF' >&2; cat "$OUT/serial.log" >&2; exit 1; fi
fi
if grep -Eiq 'PANIC|KERNEL_FAULT' "$OUT/serial.log"; then
  echo "FAIL: unexpected kernel failure marker" >&2
  exit 1
fi
echo "PASS: QEMU booted Limine and emitted KERNEL_READY on COM1"
