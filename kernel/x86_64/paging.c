#include <stdint.h>
#include <stddef.h>

/* B06: map one 4 KiB page in the active bootloader address space.
 * Intermediate tables are allocated from PMM and accessed through HHDM.
 * This does not replace CR3 or attempt to split existing huge pages. */
#define PAGE_SIZE 4096ULL
#define PRESENT 1ULL
#define WRITABLE 2ULL
#define HUGE (1ULL << 7)
#define ADDRESS_MASK 0x000ffffffffff000ULL
#define TEST_VIRTUAL 0xffffc00000000000ULL

extern uint64_t pmm_alloc(void);
extern int pmm_free(uint64_t physical);

static uint64_t direct_map;
static uint64_t mapped_frame;
static uint64_t owned_table_frames[3];
static unsigned owned_table_count;
static int allocation_budget = -1;

/* Deterministic failure injection for QEMU rollback tests. */
void paging_set_allocation_budget(int budget) { allocation_budget = budget; }
static uint64_t paging_alloc_frame(void) {
    if (allocation_budget == 0) return UINT64_MAX;
    if (allocation_budget > 0) --allocation_budget;
    return pmm_alloc();
}

static void zero_page(uint64_t *table) {
    for (unsigned i = 0; i < 512; ++i) table[i] = 0;
}
static uint64_t *table_at(uint64_t physical) {
    return (uint64_t *)(uintptr_t)(direct_map + physical);
}

int paging_init(uint64_t hhdm) {
    if (!hhdm || (hhdm & 4095)) return 0;
    direct_map = hhdm;
    mapped_frame = UINT64_MAX;
    owned_table_count = 0;
    return 1;
}

/* Replace Limine's top-level table with a kernel-owned PML4. The lower half
 * (user space from B08 on) starts empty; the higher half (kernel image, HHDM)
 * still points at Limine's PDPTs, so lower levels remain shared. */
static uint64_t kernel_pml4 = UINT64_MAX;

int paging_adopt_kernel_space(void) {
    if (!direct_map || kernel_pml4 != UINT64_MAX) return 0;
    uint64_t frame = pmm_alloc();
    if (frame == UINT64_MAX) return 0;
    uint64_t cr3;
    __asm__ volatile ("mov %%cr3, %0" : "=r"(cr3));
    const uint64_t *limine_pml4 = table_at(cr3 & ADDRESS_MASK);
    uint64_t *pml4 = table_at(frame);
    for (unsigned i = 0; i < 256; ++i) pml4[i] = 0;
    for (unsigned i = 256; i < 512; ++i) pml4[i] = limine_pml4[i];
    __asm__ volatile ("mov %0, %%cr3" : : "r"(frame) : "memory");
    __asm__ volatile ("mov %%cr3, %0" : "=r"(cr3));
    if ((cr3 & ADDRESS_MASK) != frame) return 0;
    kernel_pml4 = frame;
    return 1;
}

/* Keep each newly installed parent entry until mapping commits. On failure,
 * unlink entries before returning their backing frames to the PMM. */
int paging_map_test_page(void) {
    if (!direct_map || mapped_frame != UINT64_MAX) return 0;
    uint64_t cr3;
    __asm__ volatile ("mov %%cr3, %0" : "=r"(cr3));
    uint64_t *table = table_at(cr3 & ADDRESS_MASK);
    uint64_t *parents[3] = {0};
    uint64_t frames[3] = {0};
    unsigned indices[3] = {0};
    unsigned created = 0;
    const unsigned shifts[3] = {39, 30, 21};
    uint64_t leaf_frame = UINT64_MAX;
    int ok = 0;

    for (unsigned level = 0; level < 3; ++level) {
        unsigned index = (unsigned)((TEST_VIRTUAL >> shifts[level]) & 511);
        uint64_t entry = table[index];
        if (entry & PRESENT) {
            if (entry & HUGE || !(entry & WRITABLE)) goto rollback;
            table = table_at(entry & ADDRESS_MASK);
            continue;
        }
        uint64_t frame = paging_alloc_frame();
        if (frame == UINT64_MAX) goto rollback;
        uint64_t *child = table_at(frame);
        zero_page(child);
        parents[created] = table;
        indices[created] = index;
        frames[created] = frame;
        ++created;
        table[index] = frame | PRESENT | WRITABLE;
        table = child;
    }
    unsigned leaf = (unsigned)((TEST_VIRTUAL >> 12) & 511);
    if (table[leaf] & PRESENT) goto rollback;
    leaf_frame = paging_alloc_frame();
    if (leaf_frame == UINT64_MAX) goto rollback;
    table[leaf] = leaf_frame | PRESENT | WRITABLE;
    __asm__ volatile ("invlpg (%0)" : : "r"((uintptr_t)TEST_VIRTUAL) : "memory");
    volatile uint8_t *ptr = (volatile uint8_t *)(uintptr_t)TEST_VIRTUAL;
    ptr[0] = 0x36;
    ptr[PAGE_SIZE - 1] = 0x63;
    if (ptr[0] != 0x36 || ptr[PAGE_SIZE - 1] != 0x63) {
        table[leaf] = 0;
        __asm__ volatile ("invlpg (%0)" : : "r"((uintptr_t)TEST_VIRTUAL) : "memory");
        goto rollback;
    }
    mapped_frame = leaf_frame;
    owned_table_count = created;
    for (unsigned i = 0; i < created; ++i) owned_table_frames[i] = frames[i];
    ok = 1;
rollback:
    if (!ok) {
        if (leaf_frame != UINT64_MAX) pmm_free(leaf_frame);
        while (created) {
            --created;
            parents[created][indices[created]] = 0;
            __asm__ volatile ("invlpg (%0)" : : "r"((uintptr_t)TEST_VIRTUAL) : "memory");
            pmm_free(frames[created]);
        }
    }
    return ok;
}

/* Release only tables this module created, and only after proving that
 * their entries are empty. Never free bootloader-owned page tables. */
static int table_empty(const uint64_t *table) {
    for (unsigned i = 0; i < 512; ++i) {
        if (table[i] & PRESENT) return 0;
    }
    return 1;
}

int paging_unmap_test_page(void) {
    if (mapped_frame == UINT64_MAX) return 0;
    uint64_t cr3;
    __asm__ volatile ("mov %%cr3, %0" : "=r"(cr3));
    uint64_t *table = table_at(cr3 & ADDRESS_MASK);
    uint64_t *parents[3] = {0};
    uint64_t child_frames[3] = {0};
    unsigned indices[3] = {0};
    const unsigned shifts[3] = {39, 30, 21};
    for (unsigned level = 0; level < 3; ++level) {
        unsigned index = (unsigned)((TEST_VIRTUAL >> shifts[level]) & 511);
        uint64_t entry = table[index];
        if (!(entry & PRESENT) || (entry & HUGE)) return 0;
        parents[level] = table;
        indices[level] = index;
        child_frames[level] = entry & ADDRESS_MASK;
        table = table_at(child_frames[level]);
    }
    unsigned leaf = (unsigned)((TEST_VIRTUAL >> 12) & 511);
    if (!(table[leaf] & PRESENT) || (table[leaf] & ADDRESS_MASK) != mapped_frame) return 0;
    uint64_t leaf_frame = mapped_frame;
    table[leaf] = 0;
    __asm__ volatile ("invlpg (%0)" : : "r"((uintptr_t)TEST_VIRTUAL) : "memory");
    /* The PTE is gone and the TLB is flushed: the page is no longer mapped,
     * so clear the bookkeeping before any further step can fail and leave
     * mapped_frame pointing at a frame that is no longer reachable. */
    mapped_frame = UINT64_MAX;
    if (!pmm_free(leaf_frame)) return 0;
    for (int level = 2; level >= 0; --level) {
        uint64_t frame = child_frames[level];
        unsigned slot = owned_table_count;
        for (unsigned i = 0; i < owned_table_count; ++i) {
            if (owned_table_frames[i] == frame) { slot = i; break; }
        }
        if (slot == owned_table_count || !table_empty(table_at(frame))) break;
        parents[level][indices[level]] = 0;
        __asm__ volatile ("invlpg (%0)" : : "r"((uintptr_t)TEST_VIRTUAL) : "memory");
        /* Drop this frame from the ownership record first: whether or not the
         * PMM accepts it back, the module no longer owns the unlinked table. */
        owned_table_frames[slot] = owned_table_frames[owned_table_count - 1];
        --owned_table_count;
        if (!pmm_free(frame)) return 0;
    }
    return 1;
}
