.section .bss
buffer: .skip 4096
.section .text
.global _start
_start:
    cmpq $1, (%rsp)
    jne failure
read_next:
    xor %rax, %rax
    xor %rdi, %rdi
    lea buffer(%rip), %rsi
    mov $4096, %rdx
    syscall
    test %rax, %rax
    js failure
    jz success
    mov %rax, %r12
    lea buffer(%rip), %r13
write_next:
    mov $1, %rax
    mov $1, %rdi
    mov %r13, %rsi
    mov %r12, %rdx
    syscall
    test %rax, %rax
    jle failure
    sub %rax, %r12
    add %rax, %r13
    test %r12, %r12
    jnz write_next
    jmp read_next
success:
    xor %rdi, %rdi
    jmp exit
failure:
    mov $1, %rdi
exit:
    mov $60, %rax
    syscall
