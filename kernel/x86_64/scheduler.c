#include <stdint.h>
#include <stddef.h>

/* B07: cooperative round-robin scheduler for ring-0 kernel tasks.
 *
 * Scope (deliberately minimal and deterministic):
 *   - A fixed table of tasks, each with its own page-backed stack.
 *   - Tasks run in ring 0 and voluntarily call scheduler_yield(); preemption
 *     by the timer is B-later, user mode (ring 3) is B08.
 *   - Round-robin: yield advances to the next RUNNABLE task; a task that
 *     returns is marked FINISHED and skipped.
 *   - scheduler_run() drives the tasks from the boot context and returns once
 *     every task has finished, so the boot smoke test stays terminating.
 *
 * This does not do: priorities, sleeping/blocking, SMP, or stack-overflow
 * guard pages. Stacks are one 4 KiB heap page each. */

#define MAX_TASKS 8
#define STACK_BYTES 4096ULL

enum task_state { TASK_EMPTY = 0, TASK_RUNNABLE, TASK_FINISHED };

struct task {
    uint64_t rsp;            /* saved stack pointer when not running */
    uint8_t *stack_base;     /* page returned by heap_alloc_page (for free) */
    enum task_state state;
};

extern void context_switch(uint64_t *save_rsp, uint64_t load_rsp);
extern void task_start(void);
extern void *heap_alloc_page(void);
extern int heap_free_page(void *pointer);

static struct task tasks[MAX_TASKS];
static unsigned task_count;
static int current;              /* index of running task, -1 in boot context */
static uint64_t scheduler_rsp;   /* saved boot-context stack pointer */
static unsigned runnable_remaining;

void scheduler_init(void) {
    for (unsigned i = 0; i < MAX_TASKS; ++i) {
        tasks[i].state = TASK_EMPTY;
        tasks[i].stack_base = NULL;
        tasks[i].rsp = 0;
    }
    task_count = 0;
    current = -1;
    runnable_remaining = 0;
}

/* Returns task index >= 0, or -1 on failure (table full or no stack). */
int scheduler_spawn(void (*entry)(void *), void *arg) {
    if (!entry || task_count >= MAX_TASKS) return -1;
    uint8_t *stack = heap_alloc_page();
    if (!stack) return -1;

    /* Build the initial frame so the first context_switch resumes into
     * task_start, which then calls entry(arg). The slots below mirror the
     * pop order in context_switch (r15,r14,r13,r12,rbp,rbx) followed by the
     * return address consumed by `ret`. The stack must stay 16-byte aligned
     * at the point task_start issues its own `call`. */
    uint64_t *top = (uint64_t *)(stack + STACK_BYTES);
    /* Reserve one slot so that after the 6 pops + ret, rsp % 16 == 0 when the
     * callq inside task_start pushes its return address. */
    *--top = 0;                          /* alignment padding */
    *--top = (uint64_t)(uintptr_t)task_start; /* return address -> trampoline */
    *--top = 0;                          /* rbx */
    *--top = 0;                          /* rbp */
    *--top = (uint64_t)(uintptr_t)entry; /* r12 = entry */
    *--top = (uint64_t)(uintptr_t)arg;   /* r13 = arg */
    *--top = 0;                          /* r14 */
    *--top = 0;                          /* r15 */

    unsigned slot = task_count++;
    tasks[slot].rsp = (uint64_t)(uintptr_t)top;
    tasks[slot].stack_base = stack;
    tasks[slot].state = TASK_RUNNABLE;
    ++runnable_remaining;
    return (int)slot;
}

/* Pick the next RUNNABLE task after `from` (round-robin), or -1 if none. */
static int next_runnable(int from) {
    for (unsigned step = 1; step <= task_count; ++step) {
        unsigned i = (unsigned)((from + (int)step)) % task_count;
        if (tasks[i].state == TASK_RUNNABLE) return (int)i;
    }
    return -1;
}

/* Yield from the current task back to the scheduler loop. */
void scheduler_yield(void) {
    if (current < 0) return;             /* not inside a task */
    int me = current;
    current = -1;
    context_switch(&tasks[me].rsp, scheduler_rsp);
}

/* Called (via task_start) when a task's entry function returns. Marks it
 * finished and yields; it is never scheduled again. */
void scheduler_task_exited(void) {
    if (current < 0) return;
    int me = current;
    tasks[me].state = TASK_FINISHED;
    if (runnable_remaining) --runnable_remaining;
    current = -1;
    context_switch(&tasks[me].rsp, scheduler_rsp);
}

/* Drive all tasks round-robin from the boot context until every task has
 * finished. Returns the number of tasks that ran to completion. */
unsigned scheduler_run(void) {
    int last = -1;
    unsigned completed = 0;
    while (runnable_remaining > 0) {
        int next = next_runnable(last);
        if (next < 0) break;
        current = next;
        last = next;
        context_switch(&scheduler_rsp, tasks[next].rsp);
        /* Back in boot context. If that task finished, count it. */
        if (tasks[next].state == TASK_FINISHED) {
            ++completed;
            if (tasks[next].stack_base) {
                heap_free_page(tasks[next].stack_base);
                tasks[next].stack_base = NULL;
            }
        }
    }
    return completed;
}

unsigned scheduler_task_count(void) { return task_count; }
