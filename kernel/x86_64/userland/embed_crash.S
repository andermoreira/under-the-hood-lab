/* Embed the B12 crashing user ELF (path via -DCRASH_ELF_PATH). */
.section .rodata
.align 16
.global crash_elf_start
.global crash_elf_end
crash_elf_start:
    .incbin CRASH_ELF_PATH
crash_elf_end:

.section .note.GNU-stack,"",@progbits
