.section .rodata
message:
    .ascii "Hello from x86-64 assembly!\n"
.set message_len, . - message

.section .text
.global _start
_start:
    # Linux x86-64 syscall ABI: rax=number, rdi/rsi/rdx=args 1..3
    mov $1, %rax
    mov $1, %rdi
    lea message(%rip), %rsi
    mov $message_len, %rdx
    syscall

    # exit(0); no libc involved
    mov $60, %rax
    xor %rdi, %rdi
    syscall
