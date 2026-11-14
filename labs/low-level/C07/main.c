#include <inttypes.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

extern uint64_t add_u64(uint64_t, uint64_t, unsigned char *);
extern int64_t add_i64_overflow(int64_t, int64_t, unsigned char *);
extern uint64_t xor_mask(uint64_t, uint64_t);

static void require(int condition, const char *message) {
    if (!condition) { fprintf(stderr, "FAIL: %s\n", message); exit(1); }
}
int main(void) {
    unsigned char flag = 99;
    require(add_u64(UINT64_MAX, 1, &flag) == 0 && flag == 1, "unsigned carry");
    require(add_u64(5, 7, &flag) == 12 && flag == 0, "unsigned no carry");
    require(add_u64(UINT64_MAX, UINT64_MAX, &flag) == UINT64_MAX - 1 && flag == 1,
            "unsigned wrap");
    require(add_i64_overflow(INT64_MAX, 1, &flag) == INT64_MIN && flag == 1,
            "signed positive overflow");
    require(add_i64_overflow(INT64_MIN, -1, &flag) == INT64_MAX && flag == 1,
            "signed negative overflow");
    require(add_i64_overflow(-2, 1, &flag) == -1 && flag == 0, "signed no overflow");
    require(xor_mask(UINT64_C(0xAA55), UINT64_C(0xFFFF)) == UINT64_C(0x55AA),
            "bitwise xor");
    puts("PASS: C07 carry, overflow and bitwise operations");
    return 0;
}
