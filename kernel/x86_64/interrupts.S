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

/* #PF pushes an error code; pass it as the first argument. Fatal for now. */
.global isr_page_fault
.type isr_page_fault, @function
isr_page_fault:
    cld
    movq (%rsp), %rdi
    andq $-16, %rsp
    call exception_page_fault
2:  cli
    hlt
    jmp 2b

/* Hardware IRQ entry: preserve volatile registers, align SysV call stack,
   and return with iretq. Both IRQs are interrupt gates (IF cleared). */
.macro IRQ_ENTRY name, handler
.global \name
.type \name, @function
\name:
    cld
    pushq %rax
    pushq %rcx
    pushq %rdx
    pushq %rsi
    pushq %rdi
    pushq %r8
    pushq %r9
    pushq %r10
    pushq %r11
    pushq %r12
    movq %rsp, %r12
    andq $-16, %rsp
    call \handler
    movq %r12, %rsp
    popq %r12
    popq %r11
    popq %r10
    popq %r9
    popq %r8
    popq %rdi
    popq %rsi
    popq %rdx
    popq %rcx
    popq %rax
    iretq
.endm

IRQ_ENTRY isr_timer, irq_timer_handler
IRQ_ENTRY isr_keyboard, irq_keyboard_handler
