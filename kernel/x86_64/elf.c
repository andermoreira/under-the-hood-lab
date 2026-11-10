#include <stdint.h>
#include <stddef.h>

/* B09: minimal ELF64 loader for static ring-3 executables.
 *
 * Scope (deliberately minimal and deterministic):
 *   - Validates the ELF64 header (magic, 64-bit, little-endian, x86-64,
 *     ET_EXEC) and iterates program headers.
 *   - Maps each PT_LOAD segment page-by-page into user space with
 *     paging_map_user_page (USER|WRITABLE), copies p_filesz bytes and relies
 *     on fresh zeroed frames for the .bss tail (p_memsz > p_filesz).
 *   - Returns the entry point (e_entry).
 *
 * Not in scope: dynamic linking, relocations (ET_DYN/PIE), per-segment
 * read-only protection (everything is mapped writable for simplicity),
 * overlapping-segment coalescing, or interpreter (PT_INTERP) support. */

#define PT_LOAD 1
#define PAGE_SIZE 4096ULL

struct elf64_ehdr {
    uint8_t  e_ident[16];
    uint16_t e_type;
    uint16_t e_machine;
    uint32_t e_version;
    uint64_t e_entry;
    uint64_t e_phoff;
    uint64_t e_shoff;
    uint32_t e_flags;
    uint16_t e_ehsize;
    uint16_t e_phentsize;
    uint16_t e_phnum;
    uint16_t e_shentsize;
    uint16_t e_shnum;
    uint16_t e_shstrndx;
};

struct elf64_phdr {
    uint32_t p_type;
    uint32_t p_flags;
    uint64_t p_offset;
    uint64_t p_vaddr;
    uint64_t p_paddr;
    uint64_t p_filesz;
    uint64_t p_memsz;
    uint64_t p_align;
};

extern void *paging_map_user_page(uint64_t virt);

#define ELF_ET_EXEC 2
#define ELF_EM_X86_64 62

/* Returns 1 and sets *entry_out on success; 0 on any validation failure. */
int elf_load(const void *image, uint64_t size, uint64_t *entry_out) {
    if (!image || size < sizeof(struct elf64_ehdr)) return 0;
    const uint8_t *base = (const uint8_t *)image;
    const struct elf64_ehdr *eh = (const struct elf64_ehdr *)image;

    if (eh->e_ident[0] != 0x7f || eh->e_ident[1] != 'E' ||
        eh->e_ident[2] != 'L' || eh->e_ident[3] != 'F') return 0;
    if (eh->e_ident[4] != 2) return 0;        /* ELFCLASS64 */
    if (eh->e_ident[5] != 1) return 0;        /* ELFDATA2LSB */
    if (eh->e_type != ELF_ET_EXEC) return 0;
    if (eh->e_machine != ELF_EM_X86_64) return 0;
    if (eh->e_phentsize != sizeof(struct elf64_phdr)) return 0;
    if (eh->e_phoff + (uint64_t)eh->e_phnum * sizeof(struct elf64_phdr) > size)
        return 0;

    for (unsigned i = 0; i < eh->e_phnum; ++i) {
        const struct elf64_phdr *ph =
            (const struct elf64_phdr *)(base + eh->e_phoff +
                                        (uint64_t)i * sizeof(struct elf64_phdr));
        if (ph->p_type != PT_LOAD) continue;
        if (ph->p_filesz > ph->p_memsz) return 0;
        if (ph->p_offset + ph->p_filesz > size) return 0;
        /* User executables live in the lower canonical half. */
        if (ph->p_vaddr >= 0x0000800000000000ULL) return 0;

        uint64_t seg_start = ph->p_vaddr & ~(PAGE_SIZE - 1);
        uint64_t seg_end = ph->p_vaddr + ph->p_memsz;
        for (uint64_t page = seg_start; page < seg_end; page += PAGE_SIZE) {
            uint8_t *mapped = paging_map_user_page(page);
            if (!mapped) return 0;   /* already mapped or out of memory */
            /* Copy the slice of this segment's file image that lands in this
             * page. Bytes past p_filesz stay zero (fresh frame). */
            uint64_t copy_from = ph->p_vaddr > page ? ph->p_vaddr : page;
            uint64_t file_end = ph->p_vaddr + ph->p_filesz;
            uint64_t page_end = page + PAGE_SIZE;
            uint64_t copy_to = file_end < page_end ? file_end : page_end;
            for (uint64_t v = copy_from; v < copy_to; ++v) {
                uint64_t file_off = ph->p_offset + (v - ph->p_vaddr);
                mapped[v - page] = base[file_off];
            }
        }
    }
    *entry_out = eh->e_entry;
    return 1;
}
