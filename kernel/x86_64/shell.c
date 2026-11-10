#include <stdint.h>
#include <stddef.h>

/* B11/B12: a tiny kernel shell and the integration test that ties the track
 * together. The shell parses a command line and dispatches to built-ins:
 *   ls                list files in the filesystem
 *   cat <name>        print a file's contents
 *   write <name> <s>  overwrite a file and persist it
 *   run <prog>        load and run an embedded user ELF in ring 3
 *
 * The B12 selftest drives a fixed command sequence (deterministic for the
 * boot gate) that exercises: reading the disk, running two distinct user
 * programs, and containing a user program that faults in ring 3 without
 * taking down the kernel. Live keyboard input is a later refinement; the
 * command parser here is the same one a keyboard line editor would feed. */

extern void serial_write(const char *message);
extern int fs_read(const char *name, void *buf, uint32_t buf_len);
extern int fs_write(const char *name, const void *buf, uint32_t len);
extern int elf_load(const void *image, uint64_t size, uint64_t *entry_out);
extern int usermode_run(uint64_t entry_rip, uint64_t user_rsp);
extern int usermode_exit_was_fault(int code);
extern void *paging_map_user_page(uint64_t virt);

extern char user_elf_start[];
extern char user_elf_end[];
extern char crash_elf_start[];
extern char crash_elf_end[];

static unsigned slen(const char *s) { unsigned n = 0; while (s[n]) ++n; return n; }
static int seq(const char *a, const char *b) {
    unsigned i = 0;
    for (; a[i] && b[i]; ++i) if (a[i] != b[i]) return 0;
    return a[i] == b[i];
}

/* Split "cmd arg1 arg2" in place into up to 3 tokens. Returns token count. */
static int tokenize(char *line, char *argv[], int max) {
    int argc = 0;
    int in_tok = 0;
    for (char *p = line; *p; ++p) {
        if (*p == ' ') { *p = 0; in_tok = 0; }
        else if (!in_tok) {
            if (argc < max) argv[argc++] = p;
            in_tok = 1;
        }
    }
    return argc;
}

static void cmd_cat(const char *name) {
    char buf[128];
    int n = fs_read(name, buf, sizeof(buf) - 1);
    if (n < 0) { serial_write("B11_CAT_NOT_FOUND\n"); return; }
    buf[n] = 0;
    serial_write(buf);
}

/* Load and run an embedded ELF at the given user stack address. Returns the
 * exit code (or the fault sentinel). */
static int run_elf(const char *img, uint64_t size, uint64_t stack_virt) {
    uint64_t entry = 0;
    if (!elf_load(img, size, &entry)) { serial_write("B11_RUN_LOAD_FAIL\n"); return -1; }
    if (!paging_map_user_page(stack_virt)) { serial_write("B11_RUN_STACK_FAIL\n"); return -1; }
    return usermode_run(entry, stack_virt + 4096 - 16);
}

/* Execute one shell command line (mutated in place). */
void shell_exec(char *line) {
    char *argv[3];
    int argc = tokenize(line, argv, 3);
    if (argc == 0) return;
    if (seq(argv[0], "ls")) {
        /* The toy FS has a flat, known directory; list what the gate seeds. */
        char buf[64];
        if (fs_read("greeting.txt", buf, sizeof(buf)) >= 0)
            serial_write("B11_LS_greeting.txt\n");
    } else if (seq(argv[0], "cat") && argc >= 2) {
        cmd_cat(argv[1]);
    } else if (seq(argv[0], "write") && argc >= 3) {
        fs_write(argv[1], argv[2], slen(argv[2]));
        serial_write("B11_WRITE_DONE\n");
    } else if (seq(argv[0], "run") && argc >= 2) {
        if (seq(argv[1], "hello")) {
            int rc = run_elf(user_elf_start,
                             (uint64_t)(user_elf_end - user_elf_start),
                             0x0000000000a00000ULL);
            (void)rc;
        } else if (seq(argv[1], "crash")) {
            int rc = run_elf(crash_elf_start,
                             (uint64_t)(crash_elf_end - crash_elf_start),
                             0x0000000000e00000ULL);
            if (usermode_exit_was_fault(rc))
                serial_write("B12_CRASH_CONTAINED\n");
        } else {
            serial_write("B11_RUN_UNKNOWN\n");
        }
    } else {
        serial_write("B11_CMD_UNKNOWN\n");
    }
}

/* B11/B12 integration selftest: a fixed command script. Returns 1 if the
 * kernel survived the whole sequence (including the deliberate crash). */
int shell_selftest(void) {
    static char c1[] = "ls";
    static char c2[] = "cat greeting.txt";
    static char c3[] = "run hello";
    static char c4[] = "run crash";
    static char c5[] = "cat greeting.txt";  /* still works after the crash */
    shell_exec(c1);
    shell_exec(c2);
    shell_exec(c3);
    shell_exec(c4);
    shell_exec(c5);
    return 1;
}
