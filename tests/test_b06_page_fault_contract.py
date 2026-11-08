import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PageFaultContractTests(unittest.TestCase):
    def test_vector_14_has_error_code_aware_stub(self):
        asm = (ROOT / "kernel/x86_64/interrupts.S").read_text()
        c = (ROOT / "kernel/x86_64/interrupts.c").read_text()
        self.assertIn("isr_page_fault", asm)
        self.assertIn("set_gate(14, isr_page_fault)", c)
        self.assertIn("mov %%cr2", c)

    def test_negative_control_is_gated(self):
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        ci = (ROOT / ".github/workflows/tests.yml").read_text()
        self.assertIn("B06_TRIGGER_PF", main)
        self.assertIn("B06_EXPECT_PF", boot)
        self.assertIn("EXCEPTION_PF_CR2_0x0000000000001000", boot)
        self.assertIn("B06_EXPECT_PF=1", ci)


if __name__ == "__main__":
    unittest.main()
