#include <stdint.h>
#include <stddef.h>

struct __attribute__((packed)) descriptor_ptr {
    uint16_t limit;
    uint64_t base;
};
struct __attribute__((packed)) idt_gate {
    uint16_t offset_low;
    uint16_t selector;
    uint8_t ist;
    uint8_t attributes;
    uint16_t offset_mid;
    uint32_t offset_high;
    uint32_t reserved;
};

/* Segment loads may set the Accessed bit in GDT descriptors. Keep writable. */
static uint64_t gdt[] __attribute__((aligned(16))) = {
    0,
    0x00009a000000ffffULL, /* Limine-compatible 16-bit code */
    0x000092000000ffffULL, /* Limine-compatible 16-bit data */
    0x00cf9a000000ffffULL, /* Limine-compatible 32-bit code */
    0x00cf92000000ffffULL, /* Limine-compatible 32-bit data */
    0x00af9a000000ffffULL, /* ring-0 64-bit code, selector 0x28 */
    0x00cf92000000ffffULL  /* ring-0 data, selector 0x30 */
};
static struct idt_gate idt[256] __attribute__((aligned(16)));

extern void isr_invalid_opcode(void);
extern void serial_write(const char *message);

static void set_gate(unsigned int vector, void (*handler)(void)) {
    uintptr_t address = (uintptr_t)handler;
    idt[vector] = (struct idt_gate) {
        .offset_low = (uint16_t)address,
        .selector = 0x28,
        .ist = 0,
        .attributes = 0x8e,
        .offset_mid = (uint16_t)(address >> 16),
        .offset_high = (uint32_t)(address >> 32),
        .reserved = 0
    };
}

void interrupts_init(void) {
    struct descriptor_ptr gdtr = {sizeof(gdt) - 1, (uintptr_t)gdt};
    struct descriptor_ptr idtr = {sizeof(idt) - 1, (uintptr_t)idt};
    /* Install the exception table before changing active segments, so a
       fault during the transition is not automatically a triple fault. */
    set_gate(6, isr_invalid_opcode);
    __asm__ volatile ("cli; lidt %0" : : "m"(idtr) : "memory");
    serial_write("B03_IDT_LOADED\n");
    __asm__ volatile ("lgdt %0" : : "m"(gdtr) : "memory");
    serial_write("B03_GDT_LOADED\n");
    /* Keep the Limine-defined selector layout while replacing its GDT.
       Explicitly reload CS and the data segment caches. */
    __asm__ volatile (
        "pushq $0x28\n"
        "leaq 1f(%%rip), %%rax\n"
        "pushq %%rax\n"
        "lretq\n"
        "1:\n"
        "movw $0x30, %%ax\n"
        "movw %%ax, %%ds\n"
        "movw %%ax, %%es\n"
        "movw %%ax, %%ss\n"
        : : : "rax", "memory"
    );
    serial_write("B03_SEGMENTS_RELOADED\n");
}

__attribute__((noreturn))
void exception_invalid_opcode(void) {
    serial_write("EXCEPTION_UD_VECTOR_6\n");
    for (;;) __asm__ volatile ("cli; hlt");
}
