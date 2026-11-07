import unittest

class BitReference:
    def __init__(self):
        self.state = 0

    def clock(self, value, load):
        if load:
            self.state = value
        return self.state

class RegisterReference:
    def __init__(self, width=16):
        self.width = width
        self.state = 0

    def clock(self, value, load):
        if not (0 <= value < (1 << self.width)):
            raise ValueError("input outside register width")
        if load:
            self.state = value
        return self.state

class SequentialTests(unittest.TestCase):
    def test_bit_load_and_hold(self):
        b = BitReference()
        self.assertEqual([b.clock(v,l) for v,l in [(0,0),(1,1),(0,0),(0,1),(1,0)]],
                         [0,1,1,0,0])

    def test_register_load_and_hold(self):
        r = RegisterReference()
        self.assertEqual([r.clock(v,l) for v,l in
                         [(0,0),(0x1234,1),(0xffff,0),(0x8001,1),(0,0)]],
                         [0,0x1234,0x1234,0x8001,0x8001])

    def test_negative_control_unconditional_write(self):
        r = RegisterReference()
        r.clock(0x1234,1)
        self.assertNotEqual(r.clock(0xffff,0),0xffff)

    def test_reject_out_of_range(self):
        r = RegisterReference()
        with self.assertRaises(ValueError):
            r.clock(0x10000,1)
