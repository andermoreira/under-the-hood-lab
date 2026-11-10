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

/* #PF frame (top of stack first): error_code, RIP, CS, RFLAGS, RSP, SS.
 * Pass the error code (arg0) and the saved CS (arg1) to the C handler so it
 * can tell a ring-3 fault (CPL=3, contain it) from a ring-0 fault (fatal). */
.global isr_page_fault
.type isr_page_fault, @function
isr_page_fault:
    cld
    movq 0(%rsp), %rdi      /* error code */
    movq 16(%rsp), %rsi     /* saved CS */
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
