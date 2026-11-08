import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BuildFlagsContractTests(unittest.TestCase):
    def test_every_c_unit_pins_baseline_isa_without_simd(self):
        script = (ROOT / "scripts/build-kernel.sh").read_text()
        c_lines = [l for l in script.splitlines() if l.startswith('"$CC"') and '.c"' in l]
        self.assertGreaterEqual(len(c_lines), 6)
        for line in c_lines:
            for flag in ("-march=x86-64", "-mno-bmi2", "-mgeneral-regs-only"):
                self.assertIn(flag, line, line)


if __name__ == "__main__":
    unittest.main()
