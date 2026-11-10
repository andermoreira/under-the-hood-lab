/* Embed the linked B09 user ELF into the kernel image as a read-only blob so
 * the ELF loader has something to parse without a filesystem (disk + FS are
 * B10). The path is passed via -DUSER_ELF_PATH at assembly time. */
.section .rodata
.align 16
.global user_elf_start
.global user_elf_end
user_elf_start:
    .incbin USER_ELF_PATH
user_elf_end:

.section .note.GNU-stack,"",@progbits
