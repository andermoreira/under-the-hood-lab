.section .bss
buffer: .skip 4096
digits: .skip 32
.section .rodata
newline: .ascii "\n"
.section .text
.global _start
_start:
    cmpq $1, (%rsp)
    jne failure
    xor %r12, %r12       # bytes
    xor %r13, %r13       # newlines
read_next:
    xor %rax, %rax
    xor %rdi, %rdi
    lea buffer(%rip), %rsi
    mov $4096, %rdx
    syscall
    test %rax, %rax
    js failure
    jz print_count
    add %rax, %r12
    xor %rcx, %rcx
scan:
    cmp %rax, %rcx
    jae read_next
    cmpb $10, (%rsi,%rcx)
    jne advance
    inc %r13
advance:
    inc %rcx
    jmp scan
print_count:
    mov %r13, %rax
    call print_uint
    mov $32, %al
    mov %al, digits(%rip)
    mov $1, %rax
    mov $1, %rdi
    lea digits(%rip), %rsi
    mov $1, %rdx
    syscall
    cmp $1, %rax
    jne failure
    mov %r12, %rax
    call print_uint
    mov $1, %rax
    mov $1, %rdi
    lea newline(%rip), %rsi
    mov $1, %rdx
    syscall
    cmp $1, %rax
    jne failure
    xor %rdi, %rdi
    jmp exit
# rax unsigned number; prints decimal to stdout.
print_uint:
    lea digits+32(%rip), %r8
    mov $10, %r9
convert:
    xor %rdx, %rdx
    div %r9
    add $48, %dl
    dec %r8
    mov %dl, (%r8)
    test %rax, %rax
    jnz convert
    lea digits+32(%rip), %rdx
    sub %r8, %rdx
    mov $1, %rax
    mov $1, %rdi
    mov %r8, %rsi
    syscall
    cmp %rdx, %rax
    jne failure
    ret
failure:
    mov $1, %rdi
exit:
    mov $60, %rax
    syscall
