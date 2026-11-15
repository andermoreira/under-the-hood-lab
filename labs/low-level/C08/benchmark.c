#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

static uint64_t nanos(void) {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) { perror("clock_gettime"); exit(2); }
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}
int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: %s ITERATIONS CHUNK_BYTES\n", argv[0]); return 2; }
    char *end = NULL;
    errno = 0;
    unsigned long iterations = strtoul(argv[1], &end, 10);
    if (errno || !end || *end || !iterations || iterations > 1000000UL) return 2;
    errno = 0;
    unsigned long chunk = strtoul(argv[2], &end, 10);
    if (errno || !end || *end || !chunk || chunk > 65536UL) return 2;
    char *buf = calloc(chunk, 1);
    if (!buf) return 2;
    uint64_t start = nanos();
    for (unsigned long i = 0; i < iterations; ++i) {
        size_t written = 0;
        while (written < chunk) {
            ssize_t n = write(STDOUT_FILENO, buf + written, chunk - written);
            if (n <= 0) { perror("write"); free(buf); return 1; }
            written += (size_t)n;
        }
    }
    uint64_t elapsed = nanos() - start;
    fprintf(stderr, "C08_OK iterations=%lu chunk=%lu bytes=%llu elapsed_ns=%llu\n",
            iterations, chunk, (unsigned long long)(iterations * chunk),
            (unsigned long long)elapsed);
    free(buf);
    return 0;
}
