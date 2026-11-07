import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hack_assembler import assemble

class ProgramsTests(unittest.TestCase):
    def test_sum_program_is_valid_binary(self):
        src = (ROOT / "hardware/nand2tetris/programs/Sum1To5.asm").read_text()
        words = assemble(src).splitlines()
        self.assertGreater(len(words), 20)
        self.assertTrue(all(len(w) == 16 and set(w) <= {"0", "1"} for w in words))

    def test_loop_uses_symbolic_jump_and_variables(self):
        src = (ROOT / "hardware/nand2tetris/programs/Sum1To5.asm").read_text()
        self.assertIn("(LOOP)", src)
        self.assertIn("@END", src)
        self.assertIn("D;JEQ", src)
        self.assertIn("M=D+M", src)
        self.assertIn("M=M-1", src)

    def test_official_integration_exercises_generated_program(self):
        script = (ROOT / "hardware/nand2tetris/tests/ComputerSum.tst").read_text()
        self.assertIn("ROM32K load ../programs/Sum1To5.hack", script)
        self.assertIn("RAM16K[0]", script)
