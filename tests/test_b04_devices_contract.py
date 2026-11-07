import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class DevicesContractTests(unittest.TestCase):
    def test_irq_vectors_and_pic_mask(self):
        interrupts = (ROOT / "kernel/x86_64/interrupts.c").read_text()
        devices = (ROOT / "kernel/x86_64/devices.c").read_text()
        self.assertIn("set_gate(32, isr_timer)", interrupts)
        self.assertIn("set_gate(33, isr_keyboard)", interrupts)
        self.assertIn("outb(0x21, 0xfc)", devices)
        self.assertIn("outb(0xa1, 0xff)", devices)
        self.assertIn("outb(0x20, 0x20)", devices)
    def test_real_timer_gate(self):
        self.assertIn("timer_ticks() < 5", (ROOT / "kernel/x86_64/main.c").read_text())
        self.assertIn("B04_TIMER_TICKS_OK", (ROOT / "scripts/test-kernel-boot.sh").read_text())
    def test_keyboard_reads_controller(self):
        devices = (ROOT / "kernel/x86_64/devices.c").read_text()
        self.assertIn("inb(0x64)", devices)
        self.assertIn("inb(0x60)", devices)
        self.assertIn("B04_KEYBOARD_IRQ", devices)
