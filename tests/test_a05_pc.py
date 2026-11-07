import unittest

MASK = 0xffff

def inc16(value):
    if not 0 <= value <= MASK:
        raise ValueError("16-bit value required")
    return (value + 1) & MASK

class PC:
    def __init__(self):
        self.value = 0

    def clock(self, incoming, load=0, inc=0, reset=0):
        if not 0 <= incoming <= MASK:
            raise ValueError("16-bit value required")
        if reset:
            self.value = 0
        elif load:
            self.value = incoming
        elif inc:
            self.value = inc16(self.value)
        return self.value

class PCTests(unittest.TestCase):
    def test_inc16_boundary(self):
        self.assertEqual(inc16(0xffff),0)
        self.assertEqual(inc16(0x00ff),0x0100)

    def test_hold_increment_load_reset(self):
        pc=PC()
        self.assertEqual(pc.clock(99),0)
        self.assertEqual(pc.clock(99,inc=1),1)
        self.assertEqual(pc.clock(0x1234,load=1),0x1234)
        self.assertEqual(pc.clock(0,inc=1),0x1235)
        self.assertEqual(pc.clock(0,reset=1),0)
        self.assertEqual(pc.clock(0),0)

    def test_priority(self):
        pc=PC()
        self.assertEqual(pc.clock(0x1234,load=1,inc=1),0x1234)
        self.assertEqual(pc.clock(0x9999,load=1,inc=1,reset=1),0)

    def test_wraparound(self):
        pc=PC()
        pc.clock(0xffff,load=1)
        self.assertEqual(pc.clock(0,inc=1),0)

    def test_negative_control_inc_does_not_override_load(self):
        pc=PC()
        pc.clock(5,load=1)
        self.assertNotEqual(pc.clock(123,load=1,inc=1),6)

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            PC().clock(0x10000,load=1)
