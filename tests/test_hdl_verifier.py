import tempfile
import unittest
from pathlib import Path
from tools.verify_hdl import CHIPS, TESTS, parse, evaluate, verify

class HdlVerifierTests(unittest.TestCase):
    def test_truth_tables(self):
        for name in ("Not", "And", "Or", "Xor"):
            with self.subTest(chip=name):
                self.assertEqual(verify(name), 2 if name == "Not" else 4)

    def test_mutation_is_detected(self):
        # Replace XOR's final NAND by a direct OR-like implementation
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            for name in ("Xor",):
                original = (CHIPS / f"{name}.hdl").read_text()
                # A syntactically valid but logically wrong NAND-only circuit: OR
                mutated = """CHIP Xor {
 IN a, b;
 OUT out;
 PARTS:
 Nand(a=a,b=a,out=na);
 Nand(a=b,b=b,out=nb);
 Nand(a=na,b=nb,out=out);
}
"""
                (directory / f"{name}.hdl").write_text(mutated)
                with self.assertRaises(AssertionError):
                    verify(name, directory, TESTS)

    def test_undefined_wire_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Not.hdl"
            path.write_text("CHIP Not { IN in; OUT out; PARTS: Nand(a=missing,b=in,out=out); }")
            inputs, parts = parse(path)
            with self.assertRaises(ValueError):
                evaluate(inputs, parts, (0,))

    def test_multiple_drivers_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Not.hdl"
            path.write_text("CHIP Not { IN in; OUT out; PARTS: Nand(a=in,b=in,out=out); Nand(a=in,b=in,out=out); }")
            inputs, parts = parse(path)
            with self.assertRaises(ValueError):
                evaluate(inputs, parts, (0,))
