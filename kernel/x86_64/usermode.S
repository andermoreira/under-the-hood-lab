/* B08: ring-3 entry and SYSCALL entry stub.
 *
 * Scope: a single user task, non-reentrant syscalls. The kernel/user stack
 * pointers are swapped through globals (not per-CPU GS), which is enough for
 * the deterministic B08 smoke test and is documented as a limit. */

.section .text

/* void usermode_enter(uint64_t entry_rip, uint64_t user_rsp);
 *   %rdi = user entry point (ring-3 RIP)
 *   %rsi = user stack pointer
 * Drops to ring 3 with SYSRET. SYSRET loads CS/SS from STAR[63:48], RIP from
 * %rcx and RFLAGS from %r11. We set RFLAGS with IF=1 (0x202) so the user task
 * runs with interrupts enabled. This does not return; the user task leaves
 * ring 3 via the `syscall` instruction (see SYS_exit). */
.global usermode_enter
.type usermode_enter, @function
usermode_enter:
    movq %rsi, %rsp         /* switch to the user stack */
    movq %rdi, %rcx         /* SYSRET target RIP */
    movq $0x202, %r11       /* RFLAGS: IF=1, reserved bit 1 set */
    /* Clear the general registers we are not intentionally passing, so no
     * kernel value leaks into ring 3. */
    xorl %eax, %eax
    xorl %edi, %edi
    xorl %esi, %esi
    xorl %edx, %edx
    xorl %ebx, %ebx
    xorl %ebp, %ebp
    xorl %r8d, %r8d
    xorl %r9d, %r9d
    xorl %r10d, %r10d
    xorl %r12d, %r12d
    xorl %r13d, %r13d
    xorl %r14d, %r14d
    xorl %r15d, %r15d
    sysretq

/* SYSCALL entry. On entry: %rcx = return RIP, %r11 = saved RFLAGS, and we are
 * on the user's stack with ring-0 CS/SS already loaded by SYSCALL. The syscall
 * number is in %rax; arguments in %rdi, %rsi, %rdx (SysV-like). We save the
 * user rsp, switch to the kernel stack, call the C dispatcher, then SYSRET. */
.global syscall_entry
.type syscall_entry, @function
syscall_entry:
    movq %rsp, user_saved_rsp(%rip)   /* stash user stack */
    movq kernel_syscall_rsp(%rip), %rsp
    /* Preserve rcx (return RIP) and r11 (RFLAGS) across the C call. */
    pushq %rcx
    pushq %r11
    /* Reorder args for the SysV C ABI. User ABI: num=rax, a0=rdi, a1=rsi,
     * a2=rdx. C dispatcher: syscall_dispatch(num, a0, a1, a2) in
     * rdi, rsi, rdx, rcx. Stage a2 in r10 first to avoid clobbering. */
    movq %rdx, %r10                 /* a2 saved */
    movq %rsi, %rdx                 /* a1 -> 3rd arg (rdx) */
    movq %rdi, %rsi                 /* a0 -> 2nd arg (rsi) */
    movq %rax, %rdi                 /* num -> 1st arg (rdi) */
    movq %r10, %rcx                 /* a2 -> 4th arg (rcx) */
    call syscall_dispatch
    /* Return value in %rax stays as the user-visible result. */
    popq %r11
    popq %rcx
    movq user_saved_rsp(%rip), %rsp
    sysretq

/* void usermode_run_trampoline(uint64_t entry_rip, uint64_t user_rsp,
 *                              uint64_t *save_rsp);
 *   %rdi = entry, %rsi = user rsp, %rdx = where to save the kernel rsp.
 * Saves callee-saved registers and the kernel rsp, then enters ring 3. The
 * SYS_exit path jumps back here via usermode_return, which restores the saved
 * rsp so execution resumes at the label after the call and returns normally. */
.global usermode_run_trampoline
.type usermode_run_trampoline, @function
usermode_run_trampoline:
    pushq %rbx
    pushq %rbp
    pushq %r12
    pushq %r13
    pushq %r14
    pushq %r15
    movq %rsp, (%rdx)       /* *save_rsp = current kernel rsp */
    /* usermode_enter(entry, user_rsp) — does not return normally. */
    /* %rdi already = entry; move user_rsp into %rsi arg slot. */
    movq %rsi, %rsi         /* no-op: user_rsp already in rsi */
    call usermode_enter
    /* usermode_return lands here with rsp restored: */
.global usermode_run_resume
usermode_run_resume:
    popq %r15
    popq %r14
    popq %r13
    popq %r12
    popq %rbp
    popq %rbx
    ret

/* void usermode_return(uint64_t saved_rsp) — restore kernel rsp and resume
 * inside usermode_run_trampoline right after the call to usermode_enter. */
.global usermode_return
.type usermode_return, @function
usermode_return:
    movq %rdi, %rsp
    jmp usermode_run_resume

.section .bss
.global user_saved_rsp
.global kernel_syscall_rsp
.align 8
user_saved_rsp:    .skip 8
kernel_syscall_rsp: .skip 8

.section .note.GNU-stack,"",@progbits
