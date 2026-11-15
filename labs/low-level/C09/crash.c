#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (strcmp(argv[1], "ok") == 0) {
        puts("C09_OK");
        return 0;
    }
    if (strcmp(argv[1], "abort") == 0) {
        fputs("C09_BEFORE_ABORT\n", stderr);
        fflush(stderr);
        abort();
    }
    return 2;
}
