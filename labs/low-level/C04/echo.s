.section .rodata
space: .ascii " "
newline: .ascii "\n"
.section .text
.global _start
_start:
    mov (%rsp), %r12
    lea 16(%rsp), %r13
    xor %r14, %r14
loop_args:
    cmp $0, %r12
    jle finish
    cmp $0, %r14
    je no_space
    mov $1, %rax
    mov $1, %rdi
    lea space(%rip), %rsi
    mov $1, %rdx
    syscall
    cmp $1, %rax
    jne failure
no_space:
    mov (%r13), %rsi
    mov %rsi, %r8
length:
    cmpb $0, (%r8)
    je write_arg
    inc %r8
    jmp length
write_arg:
    sub %rsi, %r8
    jz next_arg
    mov %r8, %rdx
    mov $1, %rax
    mov $1, %rdi
    syscall
    cmp %r8, %rax
    jne failure
next_arg:
    add $8, %r13
    dec %r12
    inc %r14
    jmp loop_args
finish:
    mov $1, %rax
    mov $1, %rdi
    lea newline(%rip), %rsi
    mov $1, %rdx
    syscall
    cmp $1, %rax
    jne failure
    xor %rdi, %rdi
    jmp exit
failure:
    mov $1, %rdi
exit:
    mov $60, %rax
    syscall
