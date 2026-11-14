#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

extern long sum_seven(long, long, long, long, long, long, long);
extern long call_callback(long (*fn)(long), long);

__attribute__((noinline))
static long triple(long x) { return x * 3; }

static void check(int ok, const char *label) {
    if (!ok) {
        fprintf(stderr, "FAIL: %s\n", label);
        exit(1);
    }
    printf("PASS: %s\n", label);
}

int main(void) {
    check(sum_seven(1, 2, 3, 4, 5, 6, 7) == 28, "seven integer arguments");
    check(sum_seven(-10, 2, 0, 0, 0, 0, 1) == -7, "signed arguments");
    check(call_callback(triple, 14) == 42, "assembly calls C callback");
    check(call_callback(triple, -5) == -15, "signed callback argument");
    puts("PASS: C05 System V AMD64 ABI");
    return 0;
}
