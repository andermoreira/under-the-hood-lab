.text
.globl sum_seven
.type sum_seven, @function
# long sum_seven(long a, long b, long c, long d, long e, long f, long g)
# System V AMD64: first six integer args in rdi,rsi,rdx,rcx,r8,r9;
# seventh arg at 8(%rsp) on function entry (after return address).
sum_seven:
    lea (%rdi,%rsi), %rax
    add %rdx, %rax
    add %rcx, %rax
    add %r8, %rax
    add %r9, %rax
    add 8(%rsp), %rax
    ret
.size sum_seven, .-sum_seven

.globl call_callback
.type call_callback, @function
# long call_callback(long (*fn)(long), long value)
# Calls C callback. Stack is 16-byte aligned BEFORE call.
call_callback:
    push %rbx                  # preserves callee-saved register and aligns rsp
    mov %rdi, %rbx             # callback pointer
    mov %rsi, %rdi             # callback argument
    call *%rbx
    pop %rbx
    ret
.size call_callback, .-call_callback

.section .note.GNU-stack,"",@progbits
