#include <stdint.h>
#include <stddef.h>

/* Early kernel heap: page-sized allocations backed by Limine's HHDM.
 * The bootloader owns the initial page tables. This module does not
 * modify CR3 or map arbitrary virtual addresses. */
#define PAGE_SIZE 4096ULL
#define HEAP_SLOTS 64
#define HHDM_CANONICAL_MIN 0xffff800000000000ULL
static uint64_t hhdm_base;
static uint64_t allocated[HEAP_SLOTS];

extern uint64_t pmm_alloc(void);
extern int pmm_free(uint64_t physical);

int heap_init(uint64_t offset) {
    if (offset < HHDM_CANONICAL_MIN || (offset & (PAGE_SIZE - 1))) return 0;
    hhdm_base = offset;
    for (unsigned i = 0; i < HEAP_SLOTS; ++i) allocated[i] = UINT64_MAX;
    return 1;
}

void *heap_alloc_page(void) {
    if (!hhdm_base) return NULL;
    for (unsigned i = 0; i < HEAP_SLOTS; ++i) {
        if (allocated[i] != UINT64_MAX) continue;
        uint64_t physical = pmm_alloc();
        if (physical == UINT64_MAX) return NULL;
        if (physical > UINT64_MAX - hhdm_base) {
            pmm_free(physical);
            return NULL;
        }
        allocated[i] = physical;
        uint8_t *virtual = (uint8_t *)(uintptr_t)(hhdm_base + physical);
        for (size_t n = 0; n < PAGE_SIZE; ++n) virtual[n] = 0;
        return virtual;
    }
    return NULL;
}

int heap_free_page(void *pointer) {
    if (!pointer || !hhdm_base) return 0;
    uint64_t virtual = (uint64_t)(uintptr_t)pointer;
    if (virtual < hhdm_base) return 0;
    uint64_t physical = virtual - hhdm_base;
    if (physical & (PAGE_SIZE - 1)) return 0;
    for (unsigned i = 0; i < HEAP_SLOTS; ++i) {
        if (allocated[i] != physical) continue;
        if (!pmm_free(physical)) return 0;
        allocated[i] = UINT64_MAX;
        return 1;
    }
    return 0;
}
