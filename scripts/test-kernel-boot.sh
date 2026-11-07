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
set +e
timeout --signal=TERM --kill-after=3s 20s qemu-system-x86_64 -machine q35 -m 128M -cdrom "$OUT/kernel.iso" -boot d -display none -monitor none -serial "file:$OUT/serial.log" -no-reboot -no-shutdown >"$OUT/qemu.log" 2>&1
rc=$?
set -e
if [[ "$rc" != 124 && "$rc" != 0 ]]; then
  echo "FAIL: QEMU exited unexpectedly (status $rc)" >&2
  cat "$OUT/qemu.log" >&2
  exit 1
fi
if ! grep -Fxq 'KERNEL_READY' "$OUT/serial.log"; then
  echo "FAIL: KERNEL_READY not observed on serial console" >&2
  cat "$OUT/serial.log" "$OUT/qemu.log" >&2
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
if grep -Eiq 'PANIC|KERNEL_FAULT' "$OUT/serial.log"; then
  echo "FAIL: unexpected kernel failure marker" >&2
  exit 1
fi
echo "PASS: QEMU booted Limine and emitted KERNEL_READY on COM1"
