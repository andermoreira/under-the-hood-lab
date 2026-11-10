#include <stdint.h>
#include <stddef.h>

/* B08: minimal ring-3 support with a SYSCALL/SYSRET ABI.
 *
 * Scope (deliberately minimal and deterministic):
 *   - Configure EFER.SCE, STAR, LSTAR and SFMASK so `syscall` from ring 3
 *     traps into syscall_entry (usermode.S).
 *   - A single user task runs on its own user stack; the kernel runs syscalls
 *     on a dedicated kernel stack (swapped via globals, not per-CPU GS).
 *   - Two syscalls: SYS_write (bytes to COM1) and SYS_exit (leave ring 3).
 *
 * Not in scope here: multiple concurrent user tasks, reentrant syscalls,
 * copy-from-user validation beyond a length cap, signals, or GS-based
 * per-CPU state. Those are later steps. */

#define MSR_EFER  0xC0000080u
#define MSR_STAR  0xC0000081u
#define MSR_LSTAR 0xC0000082u
#define MSR_SFMASK 0xC0000084u
#define EFER_SCE  (1ULL << 0)
#define EFER_NXE  (1ULL << 11)

#define SYS_write 1
#define SYS_exit  2
#define USER_WRITE_MAX 256

extern void serial_write(const char *message);
extern void syscall_entry(void);
extern void tss_set_kernel_stack(uint64_t rsp0);
extern void usermode_enter(uint64_t entry_rip, uint64_t user_rsp);

/* Defined in usermode.S (.bss). The stub swaps rsp through these. */
extern uint64_t kernel_syscall_rsp;

/* Saved kernel context so SYS_exit (or a contained fault) can unwind back into
 * usermode_run(). `user_active` guards the fault path: a #PF outside a user
 * task must stay fatal. */
static uint64_t kernel_return_rsp;
static int user_exit_code;
static int user_active;

#define USER_EXIT_FAULT 0x100  /* sentinel: task was killed by a fault */

/* Returns the saved kernel rsp if a user task is currently running (so the #PF
 * handler can unwind it), or 0 otherwise. Sets the exit code to the fault
 * sentinel as a side effect. */
uint64_t usermode_fault_return_rsp(void) {
    if (!user_active) return 0;
    user_exit_code = USER_EXIT_FAULT;
    user_active = 0;
    return kernel_return_rsp;
}

static inline void wrmsr(uint32_t msr, uint64_t value) {
    __asm__ volatile ("wrmsr" : :
        "c"(msr), "a"((uint32_t)value), "d"((uint32_t)(value >> 32)));
}

/* Install the SYSCALL/SYSRET MSRs. STAR high word (bits 63:48) = 0x30 so
 * SYSRET loads SS=0x38|3 and CS=0x40|3 (our ring-3 selectors); low word
 * (bits 47:32) = 0x28 so SYSCALL loads CS=0x28 and SS=0x30 (ring 0). */
static inline uint64_t rdmsr(uint32_t msr) {
    uint32_t lo, hi;
    __asm__ volatile ("rdmsr" : "=a"(lo), "=d"(hi) : "c"(msr));
    return ((uint64_t)hi << 32) | lo;
}

void usermode_init(uint64_t kernel_stack_top) {
    /* Read EFER as EDX:EAX (not "=A", which drops the high dword) and keep all
     * existing bits. Enabling SYSCALL (SCE) must not clear NXE: Limine marks
     * read-only/kernel pages with the NX bit, and if NXE is off that bit 63
     * becomes "reserved", turning every such page into a reserved-bit #PF. */
    uint64_t efer = rdmsr(MSR_EFER);
    wrmsr(MSR_EFER, efer | EFER_SCE | EFER_NXE);
    wrmsr(MSR_STAR, ((uint64_t)0x30 << 48) | ((uint64_t)0x28 << 32));
    wrmsr(MSR_LSTAR, (uint64_t)(uintptr_t)syscall_entry);
    /* Mask IF (and DF, TF) on syscall entry so the handler runs with
     * interrupts disabled until it chooses otherwise. */
    wrmsr(MSR_SFMASK, 0x700);
    kernel_syscall_rsp = kernel_stack_top;
    tss_set_kernel_stack(kernel_stack_top);
}

/* The user write buffer lives in ring-3 memory; it is identity/HHDM mapped
 * and we only read up to a fixed cap, so a bogus pointer faults in the
 * kernel's #PF handler rather than being trusted. */
static uint64_t sys_write(const char *user_buf, uint64_t len) {
    if (len > USER_WRITE_MAX) len = USER_WRITE_MAX;
    char line[USER_WRITE_MAX + 1];
    uint64_t i = 0;
    for (; i < len; ++i) {
        char c = user_buf[i];
        if (c == 0) break;
        line[i] = c;
    }
    line[i] = 0;
    serial_write(line);
    return i;
}

/* Unwind helper implemented in usermode.S: restore kernel_return_rsp and
 * resume just after the call to usermode_enter in usermode_run(). */
extern __attribute__((noreturn)) void usermode_return(uint64_t saved_rsp);

uint64_t syscall_dispatch(uint64_t num, uint64_t a0, uint64_t a1, uint64_t a2) {
    (void)a2;
    switch (num) {
        case SYS_write:
            return sys_write((const char *)(uintptr_t)a0, a1);
        case SYS_exit:
            user_exit_code = (int)a0;
            user_active = 0;
            usermode_return(kernel_return_rsp);  /* does not return */
        default:
            serial_write("B08_SYSCALL_UNKNOWN\n");
            return (uint64_t)-1;
    }
}

/* Run one ring-3 task to completion. Returns its SYS_exit code. Implemented
 * partly in asm (usermode_run_trampoline) to capture the kernel rsp. */
extern void usermode_run_trampoline(uint64_t entry_rip, uint64_t user_rsp,
                                    uint64_t *save_rsp);

int usermode_run(uint64_t entry_rip, uint64_t user_rsp) {
    user_exit_code = -1;
    user_active = 1;
    usermode_run_trampoline(entry_rip, user_rsp, &kernel_return_rsp);
    user_active = 0;
    return user_exit_code;
}

/* Expose the fault sentinel so callers can distinguish a clean SYS_exit from a
 * contained crash. */
int usermode_exit_was_fault(int code) { return code == USER_EXIT_FAULT; }
