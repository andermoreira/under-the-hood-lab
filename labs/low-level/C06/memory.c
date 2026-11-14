#define _GNU_SOURCE
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

static int stack_value = 0; /* file-scope initialized data, not stack */
static unsigned char bss_area[4096];
static int demo_stack(int n) {
    volatile int local = n;
    printf("stack=%p data=%p bss=%p\n", (void *)&local, (void *)&stack_value, (void *)bss_area);
    return local;
}
int main(void) {
    long pagesize = sysconf(_SC_PAGESIZE);
    if (pagesize <= 0) { perror("sysconf"); return 1; }
    size_t size = (size_t)pagesize;
    unsigned char *heap = malloc(size);
    if (!heap) { perror("malloc"); return 1; }
    unsigned char *mapping = mmap(NULL, size, PROT_READ | PROT_WRITE,
                                  MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (mapping == MAP_FAILED) { perror("mmap"); free(heap); return 1; }
    heap[0] = 0x12;
    mapping[0] = 0x34;
    mapping[size - 1] = 0x56;
    if (demo_stack(42) != 42 || heap[0] != 0x12 || mapping[0] != 0x34 ||
        mapping[size - 1] != 0x56 || bss_area[0] != 0) {
        fputs("memory check failed\n", stderr);
        munmap(mapping, size); free(heap); return 1;
    }
    printf("heap=%p mmap=%p pagesize=%ld\n", (void *)heap, (void *)mapping, pagesize);
    puts("PASS: C06 memory regions and mmap");
    if (munmap(mapping, size) != 0) { perror("munmap"); free(heap); return 1; }
    free(heap);
    return 0;
}
