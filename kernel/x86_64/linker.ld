OUTPUT_FORMAT(elf64-x86-64)
ENTRY(kmain)
PHDRS {
  text PT_LOAD FLAGS(5);
  rodata PT_LOAD FLAGS(4);
  data PT_LOAD FLAGS(6);
}
SECTIONS {
  . = 0xffffffff80000000;
  .text : { *(.text .text.*) } :text
  . = ALIGN(4096);
  .rodata : {
    *(.rodata .rodata.*)
    /* B08 ring-3 payload: linked into the kernel image (read-only), then
       copied by the kernel into a user page at runtime. */
    . = ALIGN(16);
    *(.user_payload)
  } :rodata
  . = ALIGN(4096);
  .data : {
    KEEP(*(.limine_requests_start))
    KEEP(*(.limine_requests))
    KEEP(*(.limine_requests_end))
    *(.data .data.*)
  } :data
  .bss : { *(COMMON) *(.bss .bss.*) } :data
  /DISCARD/ : { *(.eh_frame*) *(.note*) }
}
