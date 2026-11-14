.section .rodata
message:
    .ascii "ELF sections and segments!\n"
.set message_len, . - message

.section .data
counter:
    .quad 42

.section .bss
    .balign 16
buffer:
    .skip 128

.section .text
.global _start
_start:
    mov $1, %rax
    mov $1, %rdi
    lea message(%rip), %rsi
    mov $message_len, %rdx
    syscall

    mov $60, %rax
    xor %rdi, %rdi
    syscall
