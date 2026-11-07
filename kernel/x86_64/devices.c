#include <stdint.h>

extern void serial_write(const char *message);
static volatile uint64_t ticks;
static volatile uint64_t keys;
static volatile uint8_t last_scancode;

static inline void outb(uint16_t port, uint8_t value) {
    __asm__ volatile ("outb %0, %1" : : "a"(value), "Nd"(port));
}
static inline uint8_t inb(uint16_t port) {
    uint8_t value;
    __asm__ volatile ("inb %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}
static void io_wait(void) { outb(0x80, 0); }
static void pic_remap(void) {
    outb(0x20, 0x11); io_wait();
    outb(0xa0, 0x11); io_wait();
    outb(0x21, 0x20); io_wait();
    outb(0xa1, 0x28); io_wait();
    outb(0x21, 0x04); io_wait();
    outb(0xa1, 0x02); io_wait();
    outb(0x21, 0x01); io_wait();
    outb(0xa1, 0x01); io_wait();
    outb(0x21, 0xfc); /* unmask IRQ0 and IRQ1 only */
    outb(0xa1, 0xff);
}
void irq_timer_handler(void) {
    ++ticks;
    outb(0x20, 0x20);
}
void irq_keyboard_handler(void) {
    serial_write("B04_IRQ1_ENTER\n");
    uint8_t status = inb(0x64);
    if (status & 1) {
        last_scancode = inb(0x60);
        ++keys;
        serial_write("B04_KEYBOARD_IRQ\n");
    }
    outb(0x20, 0x20);
}
void devices_init(void) {
    /* PIT channel 0, mode 2, ~100 Hz (1193182 / 11932). */
    pic_remap();
    outb(0x43, 0x34);
    outb(0x40, (uint8_t)(11932 & 0xff));
    outb(0x40, (uint8_t)(11932 >> 8));
    serial_write("B04_PIC_PIT_READY\n");
    __asm__ volatile ("sti" : : : "memory");
}
uint64_t timer_ticks(void) { return ticks; }
uint64_t keyboard_events(void) { return keys; }
uint8_t keyboard_last_scancode(void) { return last_scancode; }
