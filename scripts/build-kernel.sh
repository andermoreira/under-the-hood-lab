#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${KERNEL_OUT:-$ROOT/build/kernel}"
mkdir -p "$OUT"
: "${CC:=gcc}"
: "${LD:=ld}"
: "${READELF:=readelf}"
if [[ -n "${LIMINE_HEADER:-}" ]]; then
  test -f "$LIMINE_HEADER" || { echo "Missing LIMINE_HEADER: $LIMINE_HEADER" >&2; exit 2; }
  cp "$LIMINE_HEADER" "$OUT/limine.h"
elif [[ -f "$ROOT/kernel/x86_64/limine.h" ]]; then
  cp "$ROOT/kernel/x86_64/limine.h" "$OUT/limine.h"
else
  echo "NOT_RUN: set LIMINE_HEADER to an installed Limine protocol header" >&2
  exit 2
fi
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-stack-check -fno-pic -fno-pie -m64 -march=x86-64 -mno-red-zone -mcmodel=kernel -mtune=generic -mno-bmi2 -mgeneral-regs-only -fno-asynchronous-unwind-tables ${KERNEL_CFLAGS:-} -I"$OUT" -c "$ROOT/kernel/x86_64/main.c" -o "$OUT/main.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -fno-asynchronous-unwind-tables -c "$ROOT/kernel/x86_64/interrupts.c" -o "$OUT/interrupts.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/devices.c" -o "$OUT/devices.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/pmm.c" -I"$OUT" -o "$OUT/pmm.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/heap.c" -o "$OUT/heap.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/kmalloc.c" -o "$OUT/kmalloc.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/paging.c" -o "$OUT/paging.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/scheduler.c" -o "$OUT/scheduler.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/usermode.c" -o "$OUT/usermode.o"
"$CC" -m64 -c "$ROOT/kernel/x86_64/interrupts.S" -o "$OUT/interrupts_asm.o"
"$CC" -m64 -c "$ROOT/kernel/x86_64/switch.S" -o "$OUT/switch_asm.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/elf.c" -o "$OUT/elf.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/ata.c" -o "$OUT/ata.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/fs.c" -o "$OUT/fs.o"
"$CC" -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-stack-protector -fno-pic -fno-pie -m64 -mno-red-zone -mcmodel=kernel -march=x86-64 -mtune=generic -mno-bmi2 -mgeneral-regs-only -c "$ROOT/kernel/x86_64/shell.c" -o "$OUT/shell.o"
"$CC" -m64 -c "$ROOT/kernel/x86_64/usermode.S" -o "$OUT/usermode_asm.o"
"$CC" -m64 -c "$ROOT/kernel/x86_64/userprog.S" -o "$OUT/userprog_asm.o"
# B09: build the user program as its own static ELF, then embed it.
"$CC" -m64 -ffreestanding -fno-pic -c "$ROOT/kernel/x86_64/userland/hello.S" -o "$OUT/hello.o"
"$LD" -nostdlib -static -z max-page-size=0x1000 -T "$ROOT/kernel/x86_64/userland/hello.ld" "$OUT/hello.o" -o "$OUT/hello.elf"
"$CC" -m64 -DUSER_ELF_PATH="\"$OUT/hello.elf\"" -c "$ROOT/kernel/x86_64/userland/embed.S" -o "$OUT/user_elf.o"
# B12: build the deliberately-crashing user program and embed it too.
"$CC" -m64 -ffreestanding -fno-pic -c "$ROOT/kernel/x86_64/userland/crash.S" -o "$OUT/crash.o"
"$LD" -nostdlib -static -z max-page-size=0x1000 -T "$ROOT/kernel/x86_64/userland/crash.ld" "$OUT/crash.o" -o "$OUT/crash.elf"
"$CC" -m64 -DCRASH_ELF_PATH="\"$OUT/crash.elf\"" -c "$ROOT/kernel/x86_64/userland/embed_crash.S" -o "$OUT/crash_elf.o"
"$LD" -nostdlib -static -z max-page-size=0x1000 -T "$ROOT/kernel/x86_64/linker.ld" "$OUT/main.o" "$OUT/interrupts.o" "$OUT/devices.o" "$OUT/pmm.o" "$OUT/heap.o" "$OUT/kmalloc.o" "$OUT/paging.o" "$OUT/scheduler.o" "$OUT/usermode.o" "$OUT/elf.o" "$OUT/ata.o" "$OUT/fs.o" "$OUT/shell.o" "$OUT/interrupts_asm.o" "$OUT/switch_asm.o" "$OUT/usermode_asm.o" "$OUT/userprog_asm.o" "$OUT/user_elf.o" "$OUT/crash_elf.o" -o "$OUT/kernel.elf"
"$READELF" -h "$OUT/kernel.elf" | grep -q 'Machine:.*Advanced Micro Devices X86-64'
"$READELF" -h "$OUT/kernel.elf" | grep -q 'Type:.*EXEC'
"$READELF" -h "$OUT/kernel.elf" | grep -q 'Entry point address:'
if "$READELF" -d "$OUT/kernel.elf" 2>/dev/null | grep -q NEEDED; then
  echo "FAIL: kernel has dynamic dependencies" >&2
  exit 1
fi
if objdump -d "$OUT/kernel.elf" | grep -Eiq "\\b(shlx|shrx|sarx|rorx|mulx|bzhi|pdep|pext)\\b"; then
  echo "FAIL: kernel contains BMI2 instructions unsupported by baseline QEMU CPU" >&2
  objdump -d "$OUT/kernel.elf" | grep -Ei "\\b(shlx|shrx|sarx|rorx|mulx|bzhi|pdep|pext)\\b|>:$" | grep -EiB1 "\\b(shlx|shrx|sarx|rorx|mulx|bzhi|pdep|pext)\\b" | head -20 >&2
  "$CC" --version | head -1 >&2
  exit 1
fi
if [[ "${B05_DISASSEMBLE:-0}" == "1" ]]; then
  objdump -d -M intel "$OUT/kernel.elf" | sed -n '/<pmm_alloc>:/,/^$/p'
fi
echo "PASS: freestanding x86-64 kernel ELF built at $OUT/kernel.elf"
