/* Link the B09 user program as a static ELF64 executable at a fixed user-space
 * base in the lower canonical half. The kernel ELF loader maps its PT_LOAD
 * segments at these virtual addresses. */
OUTPUT_FORMAT(elf64-x86-64)
ENTRY(_start)
SECTIONS {
  . = 0x0000000000600000;
  .text : { *(.text .text.*) }
  . = ALIGN(0x1000);
  .rodata : { *(.rodata .rodata.*) }
  . = ALIGN(0x1000);
  .data : { *(.data .data.*) }
  .bss : { *(.bss .bss.*) *(COMMON) }
  /DISCARD/ : { *(.note* .eh_frame* .comment) }
}
