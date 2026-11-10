/* Link the B12 crashing user program at a user-space base distinct from the
 * hello program (0x600000), so the shell can map both without collision. */
OUTPUT_FORMAT(elf64-x86-64)
ENTRY(_start)
SECTIONS {
  . = 0x0000000000c00000;
  .text : { *(.text .text.*) }
  . = ALIGN(0x1000);
  .rodata : { *(.rodata .rodata.*) }
  . = ALIGN(0x1000);
  .data : { *(.data .data.*) }
  .bss : { *(.bss .bss.*) *(COMMON) }
  /DISCARD/ : { *(.note* .eh_frame* .comment) }
}
