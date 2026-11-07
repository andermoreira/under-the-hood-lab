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
        uint64_t frame = pmm_alloc();
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
    leaf_frame = pmm_alloc();
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

int paging_unmap_test_page(void) {
    if (mapped_frame == UINT64_MAX) return 0;
    uint64_t cr3;
    __asm__ volatile ("mov %%cr3, %0" : "=r"(cr3));
    uint64_t *table = table_at(cr3 & ADDRESS_MASK);
    unsigned shifts[] = {39, 30, 21};
    for (unsigned level = 0; level < 3; ++level) {
        uint64_t entry = table[(TEST_VIRTUAL >> shifts[level]) & 511];
        if (!(entry & PRESENT) || (entry & HUGE)) return 0;
        table = table_at(entry & ADDRESS_MASK);
    }
    unsigned leaf = (unsigned)((TEST_VIRTUAL >> 12) & 511);
    if ((table[leaf] & ADDRESS_MASK) != mapped_frame) return 0;
    table[leaf] = 0;
    __asm__ volatile ("invlpg (%0)" : : "r"((uintptr_t)TEST_VIRTUAL) : "memory");
    int freed = pmm_free(mapped_frame);
    mapped_frame = UINT64_MAX;
    /* Intermediate tables intentionally remain installed: they are
     * referenced by the active page tables and cannot be freed blindly. */
    return freed;
}
