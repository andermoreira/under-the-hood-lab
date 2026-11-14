.text
.globl add_u64
.type add_u64,@function
# uint64_t add_u64(uint64_t a, uint64_t b, unsigned char *carry)
# Return modulo 2^64; record carry flag before it can be clobbered.
add_u64:
    add %rsi, %rdi
    setc (%rdx)
    mov %rdi, %rax
    ret
.size add_u64,.-add_u64

.globl add_i64_overflow
.type add_i64_overflow,@function
# int64_t add_i64_overflow(int64_t a, int64_t b, unsigned char *overflow)
add_i64_overflow:
    add %rsi, %rdi
    seto (%rdx)
    mov %rdi, %rax
    ret
.size add_i64_overflow,.-add_i64_overflow

.globl xor_mask
.type xor_mask,@function
# uint64_t xor_mask(uint64_t value, uint64_t mask)
xor_mask:
    mov %rdi, %rax
    xor %rsi, %rax
    ret
.size xor_mask,.-xor_mask

.section .note.GNU-stack,"",@progbits
