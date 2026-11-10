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
