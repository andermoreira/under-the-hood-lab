"""Negative controls for HDL comparator: fail closed on changed data."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_cmp import check

class ComparatorNegativeControls(unittest.TestCase):
    def compare(self, expected, observed):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "expected.cmp", Path(tmp) / "actual.out"
            a.write_text(expected)
            b.write_text(observed)
            check(a, b)

    def test_equal_tables(self):
        self.compare("| a | out |\n| 0 | 1 |\n", "| a | out |\n| 0 | 1 |\n")

    def test_mutated_output_rejected(self):
        with self.assertRaisesRegex(AssertionError, "Output mismatch"):
            self.compare("| a | out |\n| 0 | 1 |\n", "| a | out |\n| 0 | 0 |\n")

    def test_missing_row_rejected(self):
        with self.assertRaisesRegex(AssertionError, "row count"):
            self.compare("| a | out |\n| 0 | 1 |\n| 1 | 0 |\n",
                         "| a | out |\n| 0 | 1 |\n")

    def test_extra_column_rejected(self):
        with self.assertRaisesRegex(AssertionError, "column count"):
            self.compare("| a | out |\n| 0 | 1 |\n",
                         "| a | out | extra |\n| 0 | 1 | 0 |\n")

    def test_malformed_table_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid or empty"):
            self.compare("| a | out |\n| 0 | 1 |\n", "0 1\n")

if __name__ == "__main__":
    unittest.main()
