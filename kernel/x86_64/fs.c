#include <stdint.h>
#include <stddef.h>

/* B10: a tiny read/write filesystem on top of the ATA driver.
 *
 * On-disk layout (512-byte sectors, little-endian):
 *   LBA 0        superblock: magic "UTHLABFS", u32 entry_count
 *   LBA 1..      directory: fixed 64-byte entries
 *   data sectors each file occupies a contiguous run starting at start_lba
 *
 * Directory entry (64 bytes):
 *   char     name[48]       NUL-padded
 *   u32      start_lba      first data sector
 *   u32      size           current file length in bytes
 *   u32      capacity       reserved sectors (max size = capacity*512)
 *   u32      reserved
 *
 * Scope: flat directory (no subdirs), fixed per-file capacity, files fit in a
 * single sector read/write path here (size capped at 512). This is enough to
 * prove persistence (write then read-back across the ATA driver). Not a POSIX
 * FS: no permissions, timestamps, fragmentation, or free-space management. */

#define SECTOR 512u
#define FS_MAGIC0 0x4241484c55ULL  /* unused numeric form; string check below */
#define DIR_LBA 1u
#define ENTRY_SIZE 64u
#define NAME_MAX 48u

extern int ata_read_sector(uint32_t lba, void *buf);
extern int ata_write_sector(uint32_t lba, const void *buf);

struct __attribute__((packed)) superblock {
    char magic[8];       /* "UTHLABFS" */
    uint32_t entry_count;
};

struct __attribute__((packed)) dirent {
    char name[NAME_MAX];
    uint32_t start_lba;
    uint32_t size;
    uint32_t capacity;
    uint32_t reserved;
};

static int str_eq(const char *a, const char *b, unsigned max) {
    for (unsigned i = 0; i < max; ++i) {
        if (a[i] != b[i]) return 0;
        if (a[i] == 0) return 1;
    }
    return 1;
}

static int fs_valid_super(const struct superblock *sb) {
    const char want[8] = {'U','T','H','L','A','B','F','S'};
    for (unsigned i = 0; i < 8; ++i) if (sb->magic[i] != want[i]) return 0;
    return 1;
}

/* Find a directory entry by name. Returns 1 and fills *out and *out_lba (the
 * directory sector holding it) on success. */
static int fs_find(const char *name, struct dirent *out, uint32_t *dir_lba,
                   unsigned *slot_in_sector) {
    uint8_t sector[SECTOR];
    if (!ata_read_sector(0, sector)) return 0;
    struct superblock sb;
    for (unsigned i = 0; i < sizeof(sb); ++i) ((uint8_t *)&sb)[i] = sector[i];
    if (!fs_valid_super(&sb)) return 0;

    unsigned per_sector = SECTOR / ENTRY_SIZE;
    for (uint32_t e = 0; e < sb.entry_count; ++e) {
        uint32_t lba = DIR_LBA + e / per_sector;
        unsigned slot = e % per_sector;
        if (!ata_read_sector(lba, sector)) return 0;
        struct dirent *de = (struct dirent *)(sector + slot * ENTRY_SIZE);
        if (str_eq(de->name, name, NAME_MAX)) {
            for (unsigned i = 0; i < sizeof(*out); ++i)
                ((uint8_t *)out)[i] = ((uint8_t *)de)[i];
            *dir_lba = lba;
            *slot_in_sector = slot;
            return 1;
        }
    }
    return 0;
}

/* Read up to buf_len bytes of `name` into buf. Returns bytes read, or -1. */
int fs_read(const char *name, void *buf, uint32_t buf_len) {
    struct dirent de;
    uint32_t dir_lba;
    unsigned slot;
    if (!fs_find(name, &de, &dir_lba, &slot)) return -1;
    uint32_t n = de.size < buf_len ? de.size : buf_len;
    if (n > SECTOR) n = SECTOR;      /* single-sector files in this build */
    uint8_t sector[SECTOR];
    if (!ata_read_sector(de.start_lba, sector)) return -1;
    for (uint32_t i = 0; i < n; ++i) ((uint8_t *)buf)[i] = sector[i];
    return (int)n;
}

/* Overwrite `name` with len bytes from buf (len <= capacity*512 and <= 512
 * here). Updates the directory size field and flushes. Returns bytes written,
 * or -1 on failure. */
int fs_write(const char *name, const void *buf, uint32_t len) {
    struct dirent de;
    uint32_t dir_lba;
    unsigned slot;
    if (!fs_find(name, &de, &dir_lba, &slot)) return -1;
    if (len > de.capacity * SECTOR || len > SECTOR) return -1;

    uint8_t sector[SECTOR];
    for (unsigned i = 0; i < SECTOR; ++i) sector[i] = 0;
    for (uint32_t i = 0; i < len; ++i) sector[i] = ((const uint8_t *)buf)[i];
    if (!ata_write_sector(de.start_lba, sector)) return -1;

    /* Update the size field in the directory sector. */
    if (!ata_read_sector(dir_lba, sector)) return -1;
    struct dirent *on_disk = (struct dirent *)(sector + slot * ENTRY_SIZE);
    on_disk->size = len;
    if (!ata_write_sector(dir_lba, sector)) return -1;
    return (int)len;
}
