/* B12: a ring-3 program that deliberately faults, to prove the kernel contains
 * a misbehaving user program instead of dying. It writes a marker, then reads
 * from an unmapped user address, triggering a #PF from ring 3. The kernel's
 * #PF handler sees CPL=3 and unwinds back to the shell. */

.section .text
.global _start
_start:
    /* SYS_write("B12_CRASH_BEFORE_FAULT\n") */
    leaq msg(%rip), %rdi
    movq $(msg_end - msg), %rsi
    movq $1, %rax
    syscall
    /* Dereference an address that is not mapped in user space. */
    movq $0x0000700000000000, %rax
    movq (%rax), %rbx
    /* Not reached. */
1:  jmp 1b

.section .rodata
msg:
    .ascii "B12_CRASH_BEFORE_FAULT\n"
msg_end:

.section .note.GNU-stack,"",@progbits
