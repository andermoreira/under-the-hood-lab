/* B08: a tiny ring-3 payload, assembled position-independent so the kernel can
 * copy it byte-for-byte into a user page at a known virtual address.
 *
 * It issues two SYSCALLs:
 *   SYS_write(1): rax=1, rdi=ptr, rsi=len   -> writes a string to COM1
 *   SYS_exit(2):  rax=2, rdi=code           -> leaves ring 3
 *
 * The string is appended right after the code (user_payload_msg) so a single
 * RIP-relative lea computes its address regardless of load address. Everything
 * stays within one page. No stack is used beyond what SYSCALL needs. */

.section .user_payload, "ax"
.global user_payload_start
.global user_payload_end
.global user_payload_msg_offset

user_payload_start:
    /* SYS_write(msg, len) */
    leaq user_payload_msg(%rip), %rdi
    movq $user_payload_msg_len, %rsi
    movq $1, %rax
    syscall
    /* SYS_exit(0) */
    xorq %rdi, %rdi
    movq $2, %rax
    syscall
    /* Should never return to here; spin just in case. */
1:  jmp 1b

user_payload_msg:
    .ascii "B08_USERLAND_HELLO\n"
    .equ user_payload_msg_len, . - user_payload_msg
user_payload_end:

.section .note.GNU-stack,"",@progbits
