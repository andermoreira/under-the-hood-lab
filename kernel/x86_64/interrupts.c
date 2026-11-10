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

/* 64-bit TSS. Only rsp0 (the ring-0 stack loaded on a ring3->ring0 transition)
 * and io_map_base matter here; the rest stays zero. */
struct __attribute__((packed)) tss64 {
    uint32_t reserved0;
    uint64_t rsp0;
    uint64_t rsp1;
    uint64_t rsp2;
    uint64_t reserved1;
    uint64_t ist[7];
    uint64_t reserved2;
    uint16_t reserved3;
    uint16_t io_map_base;
};
static struct tss64 tss __attribute__((aligned(16)));

/* Segment loads may set the Accessed bit in GDT descriptors. Keep writable.
 * Selector map (RPL in the low 2 bits):
 *   0x28 ring-0 code64, 0x30 ring-0 data, 0x38 ring-3 data, 0x40 ring-3 code64.
 * The user selectors are placed so SYSRET's STAR layout works: with
 * STAR[63:48]=0x30, SYSRET loads SS=0x30+8=0x38|3 and CS=0x30+16=0x40|3.
 * The 16-byte TSS system descriptor occupies the last two slots (0x48). */
static uint64_t gdt[] __attribute__((aligned(16))) = {
    0,
    0x00009a000000ffffULL, /* Limine-compatible 16-bit code */
    0x000092000000ffffULL, /* Limine-compatible 16-bit data */
    0x00cf9a000000ffffULL, /* Limine-compatible 32-bit code */
    0x00cf92000000ffffULL, /* Limine-compatible 32-bit data */
    0x00af9a000000ffffULL, /* ring-0 64-bit code, selector 0x28 */
    0x00cf92000000ffffULL, /* ring-0 data, selector 0x30 */
    0x00cff2000000ffffULL, /* ring-3 data, selector 0x38 (DPL=3) */
    0x00affa000000ffffULL, /* ring-3 64-bit code, selector 0x40 (DPL=3) */
    0, 0                   /* TSS descriptor (16 bytes), selector 0x48 */
};
#define TSS_SELECTOR 0x48
static struct idt_gate idt[256] __attribute__((aligned(16)));

static void install_tss(void) {
    uintptr_t base = (uintptr_t)&tss;
    uint32_t limit = sizeof(tss) - 1;
    /* Available 64-bit TSS: type=0x9, present. Two 8-byte slots. */
    uint64_t low = 0;
    low |= (uint64_t)(limit & 0xffff);
    low |= (uint64_t)(base & 0xffffff) << 16;
    low |= (uint64_t)0x89 << 40;                 /* present, type 0x9 */
    low |= (uint64_t)((limit >> 16) & 0xf) << 48;
    low |= (uint64_t)((base >> 24) & 0xff) << 56;
    uint64_t high = (base >> 32) & 0xffffffff;
    gdt[9] = low;
    gdt[10] = high;
}

/* Exposed so the usermode module can set the ring-0 stack and read the TSS
 * selector. */
void tss_set_kernel_stack(uint64_t rsp0) { tss.rsp0 = rsp0; }
uint16_t tss_selector(void) { return TSS_SELECTOR; }

extern void isr_invalid_opcode(void);
extern void isr_page_fault(void);
extern void isr_timer(void);
extern void isr_keyboard(void);
extern void irq_timer_handler(void);
extern void irq_keyboard_handler(void);
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
    set_gate(14, isr_page_fault);
    set_gate(32, isr_timer);
    set_gate(33, isr_keyboard);
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
    install_tss();
    __asm__ volatile ("ltr %w0" : : "r"((uint16_t)TSS_SELECTOR) : "memory");
    serial_write("B03_TSS_LOADED\n");
}

__attribute__((noreturn))
void exception_invalid_opcode(void) {
    serial_write("EXCEPTION_UD_VECTOR_6\n");
    for (;;) __asm__ volatile ("cli; hlt");
}

static void serial_write_hex_line(const char *prefix, uint64_t value) {
    char line[64];
    unsigned n = 0;
    while (*prefix) line[n++] = *prefix++;
    line[n++] = '0';
    line[n++] = 'x';
    for (int shift = 60; shift >= 0; shift -= 4)
        line[n++] = "0123456789abcdef"[(value >> shift) & 0xf];
    line[n++] = '\n';
    line[n] = 0;
    serial_write(line);
}

/* B11/B12: let the kernel contain a ring-3 fault instead of dying. When a user
 * task faults, unwind back into usermode_run via usermode_return (set up in
 * usermode_run_trampoline) with a nonzero code, so the shell keeps running. */
extern __attribute__((noreturn)) void usermode_return(uint64_t saved_rsp);
extern uint64_t usermode_fault_return_rsp(void);

/* Error code bits: P=0 not-present, W/R=1 write, U/S=1 user, I/D=1 fetch. */
__attribute__((noreturn))
void exception_page_fault(uint64_t error_code, uint64_t saved_cs) {
    uint64_t cr2;
    __asm__ volatile ("mov %%cr2, %0" : "=r"(cr2));
    /* CPL is the low 2 bits of the saved CS. A fault from ring 3 is a user
     * program crashing: contain it and return to the kernel. */
    if ((saved_cs & 3) == 3) {
        serial_write_hex_line("EXCEPTION_PF_USER_CR2_", cr2);
        uint64_t resume = usermode_fault_return_rsp();
        if (resume) usermode_return(resume);  /* does not return */
    }
    serial_write_hex_line("EXCEPTION_PF_CR2_", cr2);
    serial_write_hex_line("EXCEPTION_PF_ERROR_", error_code);
    for (;;) __asm__ volatile ("cli; hlt");
}
