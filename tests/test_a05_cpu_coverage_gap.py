"""Assert actual Hack CPU scenarios rather than freezing historical coverage gaps."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "hardware/nand2tetris/tests/CPU.tst"
CMP = ROOT / "hardware/nand2tetris/tests/CPU.cmp"
class CpuCoverageInventory(unittest.TestCase):
    def test_cpu_has_reset_memory_and_jump_scenarios(self):
        text = TEST.read_text()
        instructions = [line for line in text.splitlines() if line.strip().startswith("set instruction")]
        self.assertGreaterEqual(len(instructions), 13)
        self.assertTrue(any("set reset 1" in line for line in instructions))
        self.assertTrue(any("set inM 21" in line for line in instructions))
        self.assertTrue(any("1110001100001000" in line for line in instructions))
        self.assertTrue(any("1110001100000001" in line for line in instructions))
        self.assertTrue(any("1110001100000100" in line for line in instructions))
        self.assertEqual(len(instructions), len(CMP.read_text().splitlines()) - 1)
if __name__ == "__main__":
    unittest.main()
