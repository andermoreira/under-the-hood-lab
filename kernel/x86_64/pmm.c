#include <stdint.h>
#include <stddef.h>
#include "limine.h"
extern void serial_write(const char *message);

/* B05 deliberately manages only frames below 4 GiB; B06 will extend this. */
#define PAGE_SIZE 4096ULL
#define MAX_FRAMES (1ULL << 20)
static uint8_t used[MAX_FRAMES / 8];
static uint8_t owned[MAX_FRAMES / 8];
static uint64_t free_frames;
static uint64_t cursor;

static int bit_get(uint64_t i) { return (used[i >> 3] >> (i & 7)) & 1; }
static void bit_set(uint64_t i) { used[i >> 3] |= (uint8_t)(1u << (i & 7)); }
static void bit_clear(uint64_t i) { used[i >> 3] &= (uint8_t)~(1u << (i & 7)); }

void pmm_init(const struct limine_memmap_response *map) {
    for (size_t i = 0; i < sizeof(used); ++i) used[i] = 0xff;
    for (size_t i = 0; i < sizeof(owned); ++i) owned[i] = 0;
    free_frames = 0;
    cursor = 0;
    if (!map) return;
    for (uint64_t e = 0; e < map->entry_count; ++e) {
        const struct limine_memmap_entry *entry = map->entries[e];
        if (entry->type != LIMINE_MEMMAP_USABLE) continue;
        uint64_t start = entry->base / PAGE_SIZE + (entry->base % PAGE_SIZE != 0);
        uint64_t end = entry->base / PAGE_SIZE + entry->length / PAGE_SIZE;
        if ((entry->base % PAGE_SIZE) + (entry->length % PAGE_SIZE) >= PAGE_SIZE) ++end;
        if (start >= MAX_FRAMES) continue;
        if (end > MAX_FRAMES) end = MAX_FRAMES;
        for (uint64_t frame = start; frame < end; ++frame) {
            if (bit_get(frame)) { bit_clear(frame); ++free_frames; }
        }
    }
}

uint64_t pmm_free_count(void) { return free_frames; }

/* Returns physical address, or UINT64_MAX when exhausted. Frame zero is never allocated. */
uint64_t pmm_alloc(void) {
    serial_write("B05_PMM_ALLOC_ENTER\n");
    serial_write("B05_PMM_SCAN_START\n");
    for (uint64_t i = cursor; i < MAX_FRAMES; ++i) {
        if (!bit_get(i)) {
            serial_write("B05_PMM_FOUND_FRAME\n");
            bit_set(i);
            owned[i >> 3] |= (uint8_t)(1u << (i & 7));
            --free_frames;
            cursor = i + 1;
            return i * PAGE_SIZE;
        }
    }
    for (uint64_t i = 1; i < cursor; ++i) {
        if (!bit_get(i)) {
            bit_set(i);
            owned[i >> 3] |= (uint8_t)(1u << (i & 7));
            --free_frames;
            cursor = i + 1;
            return i * PAGE_SIZE;
        }
    }
    return UINT64_MAX;
}

/* Reject double-free, unaligned, zero and out-of-range frames. */
int pmm_free(uint64_t physical) {
    if (!physical || physical % PAGE_SIZE || physical / PAGE_SIZE >= MAX_FRAMES) return 0;
    uint64_t frame = physical / PAGE_SIZE;
    if (!(owned[frame >> 3] & (1u << (frame & 7)))) return 0;
    owned[frame >> 3] &= (uint8_t)~(1u << (frame & 7));
    bit_clear(frame);
    ++free_frames;
    if (frame < cursor) cursor = frame;
    return 1;
}
