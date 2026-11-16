"""Independent truth-table oracle for combinational HDL fixture values.

Does not execute HDL; the official simulator remains the behavioral gate.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "hardware/nand2tetris/tests"
CHIPS = ("Not16", "And16", "Or16", "Mux16", "DMux", "DMux4Way",
         "DMux8Way", "Mux4Way16", "Mux8Way16", "Or8Way")

def expected(chip, inputs):
    if chip == "Not16":
        return {"out": (~inputs["in"]) & 65535}
    if chip == "And16":
        return {"out": inputs["a"] & inputs["b"]}
    if chip == "Or16":
        return {"out": inputs["a"] | inputs["b"]}
    if chip in ("Mux16", "Mux4Way16", "Mux8Way16"):
        return {"out": inputs[chr(ord("a") + inputs["sel"])]}
    if chip.startswith("DMux"):
        names = "ab" if chip == "DMux" else ("abcd" if chip == "DMux4Way" else "abcdefgh")
        return {name: inputs["in"] if i == inputs["sel"] else 0 for i, name in enumerate(names)}
    if chip == "Or8Way":
        return {"out": int(inputs["in"] != 0)}
    raise ValueError(chip)

def verify_fixture(chip, directory=ROOT):
    script = (directory / (chip + ".tst")).read_text()
    table = (directory / (chip + ".cmp")).read_text()
    rows = [[x.strip() for x in line.strip().strip("|").split("|")]
            for line in table.splitlines() if line.strip().startswith("|")]
    columns = rows[0]
    cases = [line for line in script.splitlines() if line.startswith("set ")]
    if len(cases) != len(rows) - 1:
        raise AssertionError(f"{chip}: row count mismatch")
    for index, (case, row) in enumerate(zip(cases, rows[1:]), 1):
        pairs = re.findall(r"set\s+(\w+)\s+(\d+)", case)
        inputs = {name: int(value) for name, value in pairs}
        observed = dict(zip(columns, map(int, row)))
        for key, value in expected(chip, inputs).items():
            if observed[key] != value:
                raise AssertionError(f"{chip} row {index}: {key}={observed[key]} expected {value}")
    return len(cases)

class IndependentHdlFixtureOracle(unittest.TestCase):
    def test_known_combinational_fixtures(self):
        for chip in CHIPS:
            with self.subTest(chip=chip):
                self.assertGreater(verify_fixture(chip), 0)

    def test_negative_wrong_expected_value(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "Not16.tst").write_text(
                "load ../Not16.hdl,\nset in 0, eval, output;\n")
            (path / "Not16.cmp").write_text("| in | out |\n| 0 | 0 |\n")
            with self.assertRaisesRegex(AssertionError, "expected 65535"):
                verify_fixture("Not16", path)

if __name__ == "__main__":
    unittest.main()
