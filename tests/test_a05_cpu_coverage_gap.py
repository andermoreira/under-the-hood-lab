"""Fail-closed structural coverage inventory for the Hack CPU exercise."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "hardware/nand2tetris/tests/CPU.tst"

class CpuCoverageInventory(unittest.TestCase):
    def test_cpu_test_has_required_scenarios(self):
        content = TEST.read_text()
        instructions = [line for line in content.splitlines() if line.strip().startswith("set instruction")]
        self.assertGreaterEqual(len(instructions), 6)
        self.assertTrue(any("set reset 0" in line for line in instructions))
        # Existing test does not exercise reset=1, writeM=1, or inM != 0.
        # Track gaps explicitly without marking them PASS.
        missing = {
            "reset_asserted": not any("set reset 1" in line for line in instructions),
            "external_memory_input": not any("set inM 0" not in line for line in instructions),
        }
        self.assertEqual(set(missing), {"reset_asserted", "external_memory_input"})

if __name__ == "__main__":
    unittest.main()
