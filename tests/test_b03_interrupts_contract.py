import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class InterruptsContractTests(unittest.TestCase):
    def test_exception_gate_and_descriptor_tables(self):
        code = (ROOT / "kernel/x86_64/interrupts.c").read_text()
        self.assertIn("lgdt", code)
        self.assertIn("lidt", code)
        self.assertIn("set_gate(6, isr_invalid_opcode)", code)
        self.assertIn("EXCEPTION_UD_VECTOR_6", code)

    def test_real_fault_trigger(self):
        code = (ROOT / "kernel/x86_64/main.c").read_text()
        self.assertIn('ud2', code)
        self.assertIn('B03_TRIGGER_UD2', code)

    def test_ci_runs_negative_exception_scenario(self):
        workflow = (ROOT / ".github/workflows/tests.yml").read_text()
        self.assertIn("B03_TRIGGER_UD2", workflow)
        self.assertIn("EXCEPTION_UD_VECTOR_6", workflow)
