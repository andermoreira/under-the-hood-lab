/* B09: a freestanding ring-3 user program, linked as its own ELF64 executable
 * and loaded by the kernel's ELF loader at runtime.
 *
 * ABI (matches B08): syscall number in rax, args in rdi/rsi/rdx.
 *   SYS_write(1): rdi=ptr, rsi=len
 *   SYS_exit(2):  rdi=code
 * The program is position-dependent: it is linked at USER_BASE (see
 * hello.ld) and the kernel loader maps its PT_LOAD segments there. */

.section .text
.global _start
_start:
    /* SYS_write(msg, len) */
    leaq msg(%rip), %rdi
    movq $(msg_end - msg), %rsi
    movq $1, %rax
    syscall
    /* SYS_exit(0) */
    xorq %rdi, %rdi
    movq $2, %rax
    syscall
1:  jmp 1b

.section .rodata
msg:
    .ascii "B09_ELF_HELLO\n"
msg_end:

.section .note.GNU-stack,"",@progbits
