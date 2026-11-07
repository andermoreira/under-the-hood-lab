import tempfile
import unittest
from pathlib import Path
from tools.check_cmp import check, rows

class CompareTests(unittest.TestCase):
    def test_matching_table(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"a",Path(d)/"b"
            a.write_text("| a | out |\n| 0 | 1 |\n")
            b.write_text("|  a  | out |\n|  0  |  1  |\n")
            check(a,b)

    def test_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"a",Path(d)/"b"
            a.write_text("| a | out |\n| 0 | 1 |\n")
            b.write_text("| a | out |\n| 0 | 0 |\n")
            with self.assertRaises(AssertionError): check(a,b)

    def test_missing_output_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"a",Path(d)/"b"
            a.write_text("| a | out |\n| 0 | 1 |\n")
            b.write_text("")
            with self.assertRaises(ValueError): check(a,b)
