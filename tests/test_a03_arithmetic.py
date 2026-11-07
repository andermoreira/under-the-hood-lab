import unittest

MASK = (1 << 16) - 1

def add16(a, b):
    """Reference ripple-carry adder using only single-bit Boolean operations."""
    if not (0 <= a <= MASK and 0 <= b <= MASK):
        raise ValueError("Operands must be unsigned 16-bit values")
    result = 0
    carry = 0
    for bit in range(16):
        x, y = (a >> bit) & 1, (b >> bit) & 1
        s = x ^ y ^ carry
        carry = (x & y) | (carry & (x ^ y))
        result |= s << bit
    return result, carry

def signed16(value):
    return value if value < 0x8000 else value - 0x10000

def signed_overflow(a, b, result):
    """Two's-complement overflow, distinct from unsigned carry."""
    return bool((~(a ^ b) & (a ^ result) & 0x8000))

class Add16Tests(unittest.TestCase):
    def test_boundaries(self):
        cases = [(0,0), (1,1), (0xffff,1), (0x7fff,1),
                 (0x8000,0x8000), (0xffff,0xffff), (0xaaaa,0x5555)]
        for a,b in cases:
            with self.subTest(a=a,b=b):
                result,carry = add16(a,b)
                self.assertEqual(result,(a+b)&MASK)
                self.assertEqual(carry,(a+b)>>16)

    def test_single_bit_pairs(self):
        for i in range(16):
            for j in range(16):
                a,b=1<<i,1<<j
                self.assertEqual(add16(a,b)[0],(a+b)&MASK)

    def test_carry_is_not_signed_overflow(self):
        result,carry=add16(0xffff,1)
        self.assertEqual((result,carry),(0,1))
        self.assertFalse(signed_overflow(0xffff,1,result))
        result,carry=add16(0x7fff,1)
        self.assertEqual((result,carry),(0x8000,0))
        self.assertTrue(signed_overflow(0x7fff,1,result))

    def test_negative_control_missing_carry(self):
        a,b=0x00ff,1
        wrong=a^b
        self.assertNotEqual(wrong,add16(a,b)[0])

    def test_reject_out_of_range(self):
        with self.assertRaises(ValueError):
            add16(0x10000,0)
