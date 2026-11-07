.section .text
.global isr_invalid_opcode
.type isr_invalid_opcode, @function
isr_invalid_opcode:
    cld
    andq $-16, %rsp
    call exception_invalid_opcode
1:  cli
    hlt
    jmp 1b
