from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Inc16ContractTests(unittest.TestCase):
    def test_constant_is_one_not_all_ones(self):
        source = (ROOT / "hardware/nand2tetris/Inc16.hdl").read_text()
        self.assertIn("b[0]=true", source)
        self.assertIn("b[1..15]=false", source)
        self.assertNotIn("b=true,", source)

    def test_official_runner_covers_increment(self):
        runner = (ROOT / "scripts/test-hdl.sh").read_text()
        self.assertIn("Inc16", runner)
