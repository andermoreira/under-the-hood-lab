import unittest
from itertools import product
from hardware.gates.nand import nand,not_gate,and_gate,or_gate,xor_gate
class TestGates(unittest.TestCase):
    def test_not(self):
        for a in (0,1): self.assertEqual(not_gate(a),1-a)
    def test_tables(self):
        for a,b in product((0,1),repeat=2):
            self.assertEqual(nand(a,b),1-(a&b))
            self.assertEqual(and_gate(a,b),a&b)
            self.assertEqual(or_gate(a,b),a|b)
            self.assertEqual(xor_gate(a,b),a^b)
    def test_invalid(self):
        for x in (-1,2,0.5,'1',True):
            with self.assertRaises(ValueError): nand(x,1)
    def test_negative_control(self):
        self.assertNotEqual(1|1,xor_gate(1,1))
