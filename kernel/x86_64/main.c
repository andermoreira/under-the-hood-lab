#include <stdint.h>
#include <stddef.h>
#include "limine.h"

__attribute__((used, section(".limine_requests_start")))
static volatile uint64_t requests_start[] = LIMINE_REQUESTS_START_MARKER;

__attribute__((used, section(".limine_requests")))
static volatile uint64_t base_revision[] = LIMINE_BASE_REVISION(3);

__attribute__((used, section(".limine_requests")))
static volatile struct limine_hhdm_request hhdm_request = {
    .id = LIMINE_HHDM_REQUEST_ID,
    .revision = 0
};

__attribute__((used, section(".limine_requests")))
static volatile struct limine_memmap_request memmap_request = {
    .id = LIMINE_MEMMAP_REQUEST_ID,
    .revision = 0
};

__attribute__((used, section(".limine_requests_end")))
static volatile uint64_t requests_end[] = LIMINE_REQUESTS_END_MARKER;

static inline void outb(uint16_t port, uint8_t value) {
    __asm__ volatile ("outb %0, %1" : : "a"(value), "Nd"(port));
}

static inline uint8_t inb(uint16_t port) {
    uint8_t value;
    __asm__ volatile ("inb %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}

static void serial_init(void) {
    outb(0x3f8 + 1, 0x00);
    outb(0x3f8 + 3, 0x80);
    outb(0x3f8 + 0, 0x03);
    outb(0x3f8 + 1, 0x00);
    outb(0x3f8 + 3, 0x03);
    outb(0x3f8 + 2, 0xc7);
    outb(0x3f8 + 4, 0x0b);
}

void serial_write(const char *text) {
    while (*text) {
        unsigned int spins = 0;
        while (!(inb(0x3f8 + 5) & 0x20) && ++spins < 1000000) {}
        outb(0x3f8, (uint8_t)*text++);
    }
}

extern void *kmalloc(size_t size);
extern int kfree(void *pointer);
extern uint64_t pmm_free_count(void);

/* 200 objects of 32 bytes span two slab pages; 16 cycles prove reuse. */
static void *kmalloc_objects[200];
static int kmalloc_selftest(void) {
    if (kmalloc(0) || kmalloc(1025)) return 0;
    uint8_t *a = kmalloc(24);
    uint8_t *b = kmalloc(24);
    if (!a || !b || a == b || ((uintptr_t)a & 31) || ((uintptr_t)b & 31)) return 0;
    a[0] = 0x11; a[31] = 0x22; b[0] = 0x33;
    if (a[0] != 0x11 || a[31] != 0x22 || b[0] != 0x33) return 0;
    if (!kfree(a) || kfree(a) || kfree(b + 1) || kfree(NULL) || !kfree(b)) return 0;
    for (size_t size = 32; size <= 1024; size *= 2) {
        void *p = kmalloc(size);
        if (!p || ((uintptr_t)p & (size - 1)) || !kfree(p)) return 0;
    }
    uint64_t free_before_kmalloc = 0;
    for (unsigned cycle = 0; cycle < 17; ++cycle) {
        for (unsigned i = 0; i < 200; ++i) {
            kmalloc_objects[i] = kmalloc(32);
            if (!kmalloc_objects[i]) return 0;
            for (unsigned j = 0; j < i; ++j)
                if (kmalloc_objects[j] == kmalloc_objects[i]) return 0;
        }
        for (unsigned i = 0; i < 200; ++i)
            if (!kfree(kmalloc_objects[i])) return 0;
        if (cycle == 0) free_before_kmalloc = pmm_free_count();
        else if (pmm_free_count() != free_before_kmalloc) return 0;
    }
    return 1;
}

extern int paging_init(uint64_t offset);
extern int paging_adopt_kernel_space(void);
extern void paging_set_allocation_budget(int budget);
extern int paging_map_test_page(void);
extern int paging_unmap_test_page(void);
extern int heap_init(uint64_t offset);
extern void *heap_alloc_page(void);
extern int heap_free_page(void *pointer);
extern void pmm_init(const struct limine_memmap_response *map);
extern uint64_t pmm_alloc(void);
extern int pmm_free(uint64_t physical);
extern uint64_t pmm_free_count(void);
extern void interrupts_init(void);
extern void devices_init(void);
extern uint64_t timer_ticks(void);
extern void scheduler_init(void);
extern int scheduler_spawn(void (*entry)(void *), void *arg);
extern void scheduler_yield(void);
extern unsigned scheduler_run(void);
extern void usermode_init(uint64_t kernel_stack_top);
extern int usermode_run(uint64_t entry_rip, uint64_t user_rsp);
extern void *paging_map_user_page(uint64_t virt);
extern char user_payload_start[];
extern char user_payload_end[];
extern int elf_load(const void *image, uint64_t size, uint64_t *entry_out);
extern char user_elf_start[];
extern char user_elf_end[];
extern int fs_read(const char *name, void *buf, uint32_t buf_len);
extern int fs_write(const char *name, const void *buf, uint32_t len);
extern int shell_selftest(void);

/* B10 disk+FS smoke test: read the seeded file, overwrite it, read it back and
 * confirm the new contents, proving persistence through the ATA driver and the
 * toy filesystem. */
static int b10_streq(const char *a, const char *b, int n) {
    for (int i = 0; i < n; ++i) if (a[i] != b[i]) return 0;
    return 1;
}
static int filesystem_selftest(void) {
    char buf[64];
    int n = fs_read("greeting.txt", buf, sizeof(buf));
    if (n != 8 || !b10_streq(buf, "disk-v1\n", 8)) return 0;
    const char *updated = "disk-v2!\n";
    if (fs_write("greeting.txt", updated, 9) != 9) return 0;
    for (int i = 0; i < 64; ++i) buf[i] = 0;
    n = fs_read("greeting.txt", buf, sizeof(buf));
    if (n != 9 || !b10_streq(buf, updated, 9)) return 0;
    return 1;
}

/* B09 ELF-loader smoke test: parse the embedded user ELF, map its PT_LOAD
 * segments into user space, map a fresh user stack, and run it in ring 3. The
 * program issues SYS_write ("B09_ELF_HELLO") then SYS_exit, proving the loader
 * reaches a working ring-3 entry point. */
#define B09_USER_STACK 0x0000000000a00000ULL
static int elf_loader_selftest(void) {
    uint64_t entry = 0;
    uint64_t size = (uint64_t)(user_elf_end - user_elf_start);
    if (!elf_load(user_elf_start, size, &entry)) return 0;
    if (entry < 0x100000ULL || entry >= 0x0000800000000000ULL) return 0;
    void *stack = paging_map_user_page(B09_USER_STACK);
    if (!stack) return 0;
    uint64_t user_rsp = B09_USER_STACK + 4096 - 16;
    return usermode_run(entry, user_rsp) == 0;
}

/* B08 ring-3 smoke test: map a user code page and a user stack page, copy the
 * position-independent payload in, drop to ring 3, and let it issue SYS_write
 * then SYS_exit. Proves ring0->ring3 transition and the syscall round-trip. */
#define B08_USER_CODE 0x0000000000400000ULL
#define B08_USER_STACK 0x0000000000800000ULL
static uint64_t b08_kernel_syscall_stack[512]; /* 4 KiB, 16-byte aligned by type */
static int usermode_selftest(void) {
    void *code = paging_map_user_page(B08_USER_CODE);
    void *stack = paging_map_user_page(B08_USER_STACK);
    if (!code || !stack) return 0;
    size_t payload = (size_t)(user_payload_end - user_payload_start);
    if (payload == 0 || payload > 4096) return 0;
    for (size_t i = 0; i < payload; ++i)
        ((uint8_t *)code)[i] = (uint8_t)user_payload_start[i];
    /* Kernel stack top for syscalls (grows down); keep 16-byte alignment. */
    uint64_t kstack_top = (uint64_t)(uintptr_t)(b08_kernel_syscall_stack + 512);
    usermode_init(kstack_top);
    uint64_t user_rsp = B08_USER_STACK + 4096 - 16;
    int code_exit = usermode_run(B08_USER_CODE, user_rsp);
    return code_exit == 0;
}

/* B07 scheduler smoke test: three ring-0 tasks append their id to a shared
 * trace on each turn, yielding between turns. Cooperative round-robin must
 * interleave them deterministically and let each run to completion. */
#define B07_TRACE_CAP 32
static char b07_trace[B07_TRACE_CAP + 1];
static unsigned b07_trace_len;
static void b07_task(void *arg) {
    char id = (char)(uintptr_t)arg;
    for (unsigned turn = 0; turn < 3; ++turn) {
        if (b07_trace_len < B07_TRACE_CAP) b07_trace[b07_trace_len++] = id;
        scheduler_yield();
    }
}
static int scheduler_selftest(void) {
    scheduler_init();
    if (scheduler_spawn(b07_task, (void *)(uintptr_t)'A') < 0) return 0;
    if (scheduler_spawn(b07_task, (void *)(uintptr_t)'B') < 0) return 0;
    if (scheduler_spawn(b07_task, (void *)(uintptr_t)'C') < 0) return 0;
    unsigned completed = scheduler_run();
    b07_trace[b07_trace_len] = 0;
    /* Three tasks, three turns each, round-robin starting at A. */
    const char *expected = "ABCABCABC";
    for (unsigned i = 0; expected[i]; ++i)
        if (b07_trace[i] != expected[i]) return 0;
    return completed == 3 && b07_trace_len == 9;
}

__attribute__((noreturn))
void kmain(void) {
    if (!LIMINE_BASE_REVISION_SUPPORTED(base_revision)) {
        for (;;) __asm__ volatile ("cli; hlt");
    }
    serial_init();
    serial_write("B03_BEFORE_TABLES\n");
    interrupts_init();
    serial_write("B03_AFTER_TABLES\n");
    serial_write("KERNEL_READY\n");
    serial_write("B05_BEFORE_PMM_INIT\n");
    if (!memmap_request.response) serial_write("B06_MEMMAP_RESPONSE_NULL\n");
    else if (!memmap_request.response->entry_count) serial_write("B06_MEMMAP_EMPTY\n");
    else serial_write("B06_MEMMAP_PRESENT\n");
    if (!hhdm_request.response) serial_write("B06_HHDM_RESPONSE_NULL\n");
    else serial_write("B06_HHDM_PRESENT\n");
    pmm_init(memmap_request.response);
    serial_write("B05_AFTER_PMM_INIT\n");
    if (pmm_free_count() < 2) { serial_write("B05_PMM_NO_MEMORY\n"); for (;;) __asm__ volatile ("cli; hlt"); }
    serial_write("B05_BEFORE_ALLOC\n");
    uint64_t first = pmm_alloc();
    uint64_t second = pmm_alloc();
    serial_write("B05_AFTER_ALLOC\n");
    if (first == UINT64_MAX || second == UINT64_MAX || first == second || !pmm_free(first) || pmm_free(first)) {
        serial_write("B05_PMM_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    serial_write("B05_PMM_ALLOC_FREE_OK\n");
    if (!hhdm_request.response || !heap_init(hhdm_request.response->offset)) {
        serial_write("B06_HEAP_INIT_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    uint8_t *page = heap_alloc_page();
    if (!page) { serial_write("B06_HEAP_ALLOC_FAIL\n"); for (;;) __asm__ volatile ("cli; hlt"); }
    for (size_t i = 0; i < 4096; ++i) {
        if (page[i] != 0) { serial_write("B06_HEAP_ZERO_FAIL\n"); for (;;) __asm__ volatile ("cli; hlt"); }
    }
    page[0] = 0xa5;
    page[4095] = 0x5a;
    if (page[0] != 0xa5 || page[4095] != 0x5a || !heap_free_page(page) || heap_free_page(page)) {
        serial_write("B06_HEAP_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    if (heap_free_page(NULL) || heap_free_page((void *)(page + 1))) {
        serial_write("B06_HEAP_INVALID_FREE_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    uint64_t free_before_heap_reuse = pmm_free_count();
    for (unsigned cycle = 0; cycle < 16; ++cycle) {
        uint8_t *reused = heap_alloc_page();
        if (!reused || reused[0] != 0 || reused[4095] != 0 ||
            !heap_free_page(reused) || pmm_free_count() != free_before_heap_reuse) {
            serial_write("B06_HEAP_REUSE_FAIL\n");
            for (;;) __asm__ volatile ("cli; hlt");
        }
    }
    serial_write("B06_HEAP_REUSE_OK\n");
    serial_write("B06_HEAP_PAGE_OK\n");
    if (!kmalloc_selftest()) {
        serial_write("B06_KMALLOC_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    serial_write("B06_KMALLOC_OK\n");
    if (!paging_init(hhdm_request.response->offset)) {
        serial_write("B06_PAGING_INIT_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    if (!paging_adopt_kernel_space() || paging_adopt_kernel_space()) {
        serial_write("B06_OWN_PML4_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    serial_write("B06_OWN_PML4_OK\n");
    uint64_t free_before_paging = pmm_free_count();
    for (int budget = 0; budget < 4; ++budget) {
        paging_set_allocation_budget(budget);
        if (paging_map_test_page() || pmm_free_count() != free_before_paging) {
            serial_write("B06_PAGING_ROLLBACK_FAIL\n");
            for (;;) __asm__ volatile ("cli; hlt");
        }
    }
    paging_set_allocation_budget(-1);
    serial_write("B06_PAGING_ROLLBACK_OK\n");
    if (!paging_map_test_page() ||
        paging_map_test_page() || !paging_unmap_test_page() || paging_unmap_test_page() ||
        pmm_free_count() != free_before_paging) {
        serial_write("B06_PAGING_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    for (unsigned cycle = 0; cycle < 16; ++cycle) {
        if (!paging_map_test_page() || !paging_unmap_test_page() ||
            pmm_free_count() != free_before_paging) {
            serial_write("B06_PAGING_REUSE_FAIL\n");
            for (;;) __asm__ volatile ("cli; hlt");
        }
    }
    serial_write("B06_PAGING_REUSE_OK\n");
    serial_write("B06_PAGING_MAP_UNMAP_OK\n");
    if (!scheduler_selftest()) {
        serial_write("B07_SCHEDULER_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    serial_write("B07_SCHEDULER_TRACE_");
    serial_write(b07_trace);
    serial_write("\n");
    serial_write("B07_SCHEDULER_OK\n");
    if (!usermode_selftest()) {
        serial_write("B08_USERMODE_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    serial_write("B08_USERMODE_OK\n");
    if (!elf_loader_selftest()) {
        serial_write("B09_ELF_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    serial_write("B09_ELF_OK\n");
    /* B09 just consumed the hello ELF's user addresses (0x600000 code,
     * 0xa00000 stack). Release them so the shell's `run hello` can map the
     * same ET_EXEC image again. */
    extern void paging_unmap_user_page(uint64_t virt);
    paging_unmap_user_page(0x0000000000600000ULL);
    paging_unmap_user_page(0x0000000000601000ULL);
    paging_unmap_user_page(0x0000000000a00000ULL);
    if (!filesystem_selftest()) {
        serial_write("B10_FS_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    serial_write("B10_FS_OK\n");
    if (!shell_selftest()) {
        serial_write("B11_SHELL_FAIL\n");
        for (;;) __asm__ volatile ("cli; hlt");
    }
    serial_write("B11_SHELL_OK\n");
    devices_init();
    while (timer_ticks() < 5) __asm__ volatile ("hlt");
    serial_write("B04_TIMER_TICKS_OK\n");
#ifdef B06_TRIGGER_PF
    /* Lower half of the kernel-owned PML4 is empty: this read must fault. */
    (void)*(volatile uint64_t *)(uintptr_t)0x1000;
#endif
#ifdef B03_TRIGGER_UD2
    __asm__ volatile ("ud2");
#endif
    for (;;) __asm__ volatile ("hlt");
}
