"""Cross-check: the Python reference models must reproduce the golden `.cmp`
tables used by the official HardwareSimulator.

REVIEW-2026-11 finding (hardware #3): the Python models and the `.cmp` tables
were each trusted on their own and never compared against each other, so a bug
in either could pass unnoticed. This test closes that gap by replaying every
input row of the golden tables through the model and asserting the model's
output equals the recorded output column.

Hypothesis: model(inputs) == golden out, for every row.
Observation: produced by running this test (see Makefile `make verify`).
A deliberate failure (negative control) is included to prove the check bites.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
TESTS = ROOT / "hardware" / "nand2tetris" / "tests"

from tests.test_alu_reference import alu  # noqa: E402
from tests.test_a03_arithmetic import add16  # noqa: E402

MASK = 0xFFFF


def inc16(value):
    """Reference for Inc16: wrap-around 16-bit increment."""
    return (value + 1) & MASK


def parse_cmp(path):
    """Yield rows of a `.cmp` table as lists of column (header, value) ints.

    Columns are hex when 4 chars wide (buses), decimal otherwise (control/flag
    bits). Returns (headers, rows) with each cell already parsed to int.
    """
    lines = [ln.strip() for ln in path.read_text().splitlines() if ln.strip()]
    rows = [[c.strip() for c in ln.strip("|").split("|")] for ln in lines]
    headers = rows[0]
    parsed = []
    for row in rows[1:]:
        cells = []
        for cell in row:
            cells.append(int(cell, 16) if len(cell) == 4 else int(cell))
        parsed.append(cells)
    return headers, parsed


class ModelMatchesGoldenTableTests(unittest.TestCase):
    def test_alu_model_reproduces_cmp(self):
        headers, rows = parse_cmp(TESTS / "ALU.cmp")
        self.assertEqual(
            headers,
            ["x", "y", "zx", "nx", "zy", "ny", "f", "no", "out", "zr", "ng"],
        )
        for row in rows:
            x, y, zx, nx, zy, ny, f, no, out, zr, ng = row
            with self.subTest(row=row):
                got_out, got_zr, got_ng = alu(x, y, zx, nx, zy, ny, f, no)
                self.assertEqual((got_out, got_zr, got_ng), (out, zr, ng))

    def test_add16_model_reproduces_cmp(self):
        headers, rows = parse_cmp(TESTS / "Add16.cmp")
        self.assertEqual(headers, ["a", "b", "out"])
        for a, b, out in rows:
            with self.subTest(a=a, b=b):
                self.assertEqual(add16(a, b)[0], out)

    def test_inc16_model_reproduces_cmp(self):
        headers, rows = parse_cmp(TESTS / "Inc16.cmp")
        self.assertEqual(headers, ["in", "out"])
        for value, out in rows:
            with self.subTest(value=value):
                self.assertEqual(inc16(value), out)

    def test_negative_control_wrong_model_is_detected(self):
        # A broken "adder" that drops the carry must disagree with the table,
        # proving the comparison is not vacuous.
        _, rows = parse_cmp(TESTS / "Add16.cmp")
        mismatches = sum(1 for a, b, out in rows if (a ^ b) != out)
        self.assertGreater(mismatches, 0)


if __name__ == "__main__":
    unittest.main()
