/* B07: cooperative context switch (ring 0).
 *
 * void context_switch(uint64_t *save_rsp, uint64_t load_rsp);
 *   %rdi = address where the current task's stack pointer is stored
 *   %rsi = stack pointer of the task to resume
 *
 * Only the System V AMD64 callee-saved registers (rbx, rbp, r12-r15) need to
 * be preserved across a function call, so those are all we push. The return
 * address is already on the stack from `call`. Switching %rsp swaps which
 * task's saved frame we pop, and `ret` jumps into the resumed task.
 *
 * A brand-new task is bootstrapped by task_start (below): its initial stack is
 * laid out so this same `ret` sequence enters the task's entry point. */
.section .text
.global context_switch
.type context_switch, @function
context_switch:
    pushq %rbx
    pushq %rbp
    pushq %r12
    pushq %r13
    pushq %r14
    pushq %r15
    movq %rsp, (%rdi)      /* save current rsp into *save_rsp */
    movq %rsi, %rsp        /* load resumed task's rsp */
    popq %r15
    popq %r14
    popq %r13
    popq %r12
    popq %rbp
    popq %rbx
    ret

/* void task_start(void);
 * Trampoline used as the initial return address of a fresh task. The task's
 * entry function pointer and its argument were planted on the new stack by
 * scheduler_spawn in the slots this trampoline expects (r12 = entry, r13 =
 * arg). On first resume, context_switch's `ret` lands here. */
.global task_start
.type task_start, @function
task_start:
    movq %r13, %rdi        /* arg */
    callq *%r12            /* entry(arg) */
    /* A task entry must not return; if it does, hand control back to the
     * scheduler, which treats a returned task as finished. */
    call scheduler_task_exited
1:  hlt
    jmp 1b

.section .note.GNU-stack,"",@progbits
