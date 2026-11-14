.section .rodata
usage:
    .ascii "usage: copy INPUT OUTPUT\n"
.set usage_len, . - usage
error:
    .ascii "copy: syscall failed\n"
.set error_len, . - error

.section .bss
    .balign 16
buffer:
    .skip 4096

.section .text
.global _start
_start:
    # Linux process stack: argc at (%rsp), argv pointers follow.
    cmpq $3, (%rsp)
    jne bad_args
    mov 16(%rsp), %rsi
    mov $257, %rax            # openat(AT_FDCWD, argv[1], O_RDONLY, 0)
    mov $-100, %rdi
    xor %rdx, %rdx
    xor %r10, %r10
    syscall
    test %rax, %rax
    js syscall_error
    mov %rax, %r12            # input fd

    mov 24(%rsp), %rsi
    mov $257, %rax            # openat(AT_FDCWD, argv[2], O_WRONLY|O_CREAT|O_TRUNC, 0644)
    mov $-100, %rdi
    mov $577, %rdx
    mov $420, %r10
    syscall
    test %rax, %rax
    js syscall_error
    mov %rax, %r13            # output fd

read_next:
    xor %rax, %rax            # read(input, buffer, 4096)
    mov %r12, %rdi
    lea buffer(%rip), %rsi
    mov $4096, %rdx
    syscall
    test %rax, %rax
    js syscall_error
    jz done
    mov %rax, %r14            # bytes remaining
    lea buffer(%rip), %r15    # current pointer

write_next:
    mov $1, %rax              # write(output, ptr, remaining)
    mov %r13, %rdi
    mov %r15, %rsi
    mov %r14, %rdx
    syscall
    test %rax, %rax
    jle syscall_error         # includes zero-progress write
    sub %rax, %r14
    add %rax, %r15
    test %r14, %r14
    jnz write_next
    jmp read_next

done:
    mov $3, %rax              # close output
    mov %r13, %rdi
    syscall
    test %rax, %rax
    js syscall_error
    mov $3, %rax              # close input
    mov %r12, %rdi
    syscall
    test %rax, %rax
    js syscall_error
    xor %rdi, %rdi
    jmp exit

bad_args:
    mov $1, %rax
    mov $2, %rdi
    lea usage(%rip), %rsi
    mov $usage_len, %rdx
    syscall
    mov $2, %rdi
    jmp exit

syscall_error:
    mov $1, %rax
    mov $2, %rdi
    lea error(%rip), %rsi
    mov $error_len, %rdx
    syscall
    mov $1, %rdi
exit:
    mov $60, %rax
    syscall
