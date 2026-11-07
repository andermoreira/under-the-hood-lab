# B04 — PIT timer and PS/2 keyboard IRQs

## Goal
Observe hardware IRQ0 (PIT timer) and IRQ1 (PS/2 keyboard) through a remapped legacy 8259 PIC, in QEMU.

## Hardware contract
- Remap PIC vectors to 0x20–0x2f, mask all but IRQ0 and IRQ1.
- PIT channel 0 runs at approximately 100 Hz using divisor 11932.
- IDT vectors 32/33 enter assembly stubs which save registers, align stack, call C handlers, acknowledge PIC, then iretq.
- Timer counter is monotonic. Five real timer interrupts emit B04_TIMER_TICKS_OK.
- Keyboard handler reads status 0x64 and scancode port 0x60 and emits B04_KEYBOARD_IRQ on an event.

## Evidence and limitations
The boot gate requires five actual timer IRQs, not merely PIT configuration. The keyboard IRQ is wired but **automated key injection is not yet covered by the QEMU gate**; do not claim end-to-end keyboard validation. The driver reports raw PS/2 scancodes only; no keymap, ring buffer, input line discipline, APIC, USB, or SMP. Existing #UD negative-control boot remains mandatory.

## Reproduction
Run `make test-kernel-boot` with Limine and QEMU installed. Inspect `build/kernel/serial.log` for KERNEL_READY, B04_PIC_PIT_READY, and B04_TIMER_TICKS_OK. Inject a key through QEMU monitor to observe B04_KEYBOARD_IRQ.
