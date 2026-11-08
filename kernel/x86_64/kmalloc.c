#include <stdint.h>
#include <stddef.h>

/* Small-object allocator: power-of-two size classes (32..1024 bytes), each
 * slab is one 4 KiB heap page with a header at its start. Objects start at
 * the first multiple of their size past the header, so they are naturally
 * aligned. A per-slab bitmap rejects double and misaligned frees. Empty
 * slabs are kept for reuse (never returned to the page heap). Memory is not
 * zeroed on reuse. */
#define PAGE_SIZE 4096ULL
#define MIN_OBJECT 32
#define MAX_OBJECT 1024
#define CLASS_COUNT 6
#define SLAB_MAGIC 0x534c4142u

struct slab {
    uint32_t magic;
    uint16_t size;
    uint16_t capacity;
    struct slab *next;
    uint64_t used[2];
};

extern void *heap_alloc_page(void);
static struct slab *classes[CLASS_COUNT];

static unsigned first_offset(unsigned size) {
    return size >= sizeof(struct slab) ? size : (unsigned)sizeof(struct slab);
}

void *kmalloc(size_t size) {
    if (!size || size > MAX_OBJECT) return NULL;
    unsigned class = 0, object = MIN_OBJECT;
    while (object < size) { object <<= 1; ++class; }
    for (struct slab *s = classes[class];; s = s->next) {
        if (!s) {
            s = heap_alloc_page();
            if (!s) return NULL;
            s->magic = SLAB_MAGIC;
            s->size = (uint16_t)object;
            s->capacity = (uint16_t)((PAGE_SIZE - first_offset(object)) / object);
            s->next = classes[class];
            classes[class] = s;
        }
        for (unsigned i = 0; i < s->capacity; ++i) {
            if (s->used[i >> 6] & (1ULL << (i & 63))) continue;
            s->used[i >> 6] |= 1ULL << (i & 63);
            return (uint8_t *)s + first_offset(object) + (size_t)i * object;
        }
    }
}

int kfree(void *pointer) {
    if (!pointer) return 0;
    struct slab *s = (struct slab *)((uintptr_t)pointer & ~(uintptr_t)(PAGE_SIZE - 1));
    if (s->magic != SLAB_MAGIC) return 0;
    uintptr_t offset = (uintptr_t)pointer - (uintptr_t)s;
    unsigned start = first_offset(s->size);
    if (offset < start || (offset - start) % s->size) return 0;
    unsigned i = (unsigned)((offset - start) / s->size);
    if (i >= s->capacity || !(s->used[i >> 6] & (1ULL << (i & 63)))) return 0;
    s->used[i >> 6] &= ~(1ULL << (i & 63));
    return 1;
}
