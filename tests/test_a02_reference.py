import itertools
import unittest

class A02ReferenceTests(unittest.TestCase):
    def test_mux_exhaustive(self):
        for a,b,sel in itertools.product((0,1), repeat=3):
            self.assertEqual(((a & (1-sel)) | (b & sel)), b if sel else a)

    def test_half_adder_exhaustive(self):
        for a,b in itertools.product((0,1), repeat=2):
            total=a+b
            self.assertEqual((a^b,a&b),(total%2,total//2))

    def test_full_adder_exhaustive(self):
        for a,b,c in itertools.product((0,1), repeat=3):
            s1=a^b
            s=s1^c
            carry=(a&b)|(s1&c)
            self.assertEqual((s,carry),((a+b+c)%2,(a+b+c)//2))

    def test_negative_control_xor_not_or(self):
        self.assertNotEqual(1^1,1|1)
