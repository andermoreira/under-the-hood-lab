"""Structural contract for Nand2Tetris fixtures; not a simulator substitute."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "hardware/nand2tetris/tests"

def inspect_fixture(tst, cmp):
    source = tst.read_text()
    rows = [line for line in cmp.read_text().splitlines() if line.strip().startswith("|")]
    if len(rows) < 2:
        raise ValueError(f"{cmp.name}: no expected rows")
    expected_cols = [c.strip() for c in rows[0].strip("|").split("|")]
    if any(len([c for c in row.strip("|").split("|")]) != len(expected_cols) for row in rows[1:]):
        raise ValueError(f"{cmp.name}: inconsistent column count")
    declaration = re.search(r"^output-list\s+(.+);$", source, re.M)
    if not declaration:
        raise ValueError(f"{tst.name}: missing output-list")
    signals = [part.split("%")[0] for part in declaration.group(1).split()]
    if signals != expected_cols:
        raise ValueError(f"{tst.name}: output-list fields differ from compare header")
    outputs = len(re.findall(r"\boutput\s*;", source))
    if outputs != len(rows) - 1:
        raise ValueError(f"{tst.name}: {outputs} outputs vs {len(rows)-1} comparison rows")
    if not re.search(r"^load\s+\S+\.hdl\s*,", source, re.M):
        raise ValueError(f"{tst.name}: missing HDL load")
    return outputs

class HdlFixtureIntegrity(unittest.TestCase):
    def test_all_fixture_pairs(self):
        for tst in sorted(TESTS.glob("*.tst")):
            with self.subTest(tst=tst.name):
                cmp = tst.with_suffix(".cmp")
                self.assertTrue(cmp.exists(), f"{tst.name} has no cmp")
                inspect_fixture(tst, cmp)

    def test_negative_unnamed_output_list(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tst = Path(tmp) / "Sample.tst"
            cmp = Path(tmp) / "Sample.cmp"
            tst.write_text("load ../Sample.hdl,\\noutput-list %B1.1.1 %B1.1.1;\\noutput;\\n")
            cmp.write_text("| a | out |\\n| 0 | 1 |\\n")
            with self.assertRaisesRegex(ValueError, "output-list fields"):
                inspect_fixture(tst, cmp)

    def test_negative_missing_output(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tst = Path(tmp) / "Sample.tst"
            cmp = Path(tmp) / "Sample.cmp"
            tst.write_text("load ../Sample.hdl,\noutput-list a%B1.1.1 out%B1.1.1;\noutput;\n")
            cmp.write_text("| a | out |\n| 0 | 0 |\n| 1 | 1 |\n")
            with self.assertRaisesRegex(ValueError, "outputs vs"):
                inspect_fixture(tst, cmp)

if __name__ == "__main__":
    unittest.main()
