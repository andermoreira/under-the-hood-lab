import unittest

class RAM:
    def __init__(self, words):
        self.words = [0] * words

    def cycle(self, address, value, load):
        if not (0 <= address < len(self.words)):
            raise ValueError("address out of range")
        if not (0 <= value <= 0xffff):
            raise ValueError("word out of range")
        if load:
            self.words[address] = value
        return self.words[address]

class RAMTests(unittest.TestCase):
    def test_independent_addresses(self):
        for size in (8,64):
            with self.subTest(size=size):
                ram=RAM(size)
                ram.cycle(0,0x1234,1)
                ram.cycle(size-1,0xabcd,1)
                self.assertEqual(ram.cycle(0,0xffff,0),0x1234)
                self.assertEqual(ram.cycle(size-1,0,0),0xabcd)
                self.assertEqual(ram.cycle(size//2,0,0),0)

    def test_all_addresses(self):
        for size in (8,64):
            ram=RAM(size)
            for i in range(size):
                ram.cycle(i,(i*1009)&0xffff,1)
            for i in range(size):
                self.assertEqual(ram.cycle(i,0,0),(i*1009)&0xffff)

    def test_negative_control_aliasing(self):
        ram=RAM(8)
        ram.cycle(0,1,1)
        ram.cycle(4,2,1)
        self.assertNotEqual(ram.cycle(0,0,0),ram.cycle(4,0,0))

    def test_invalid_address(self):
        with self.assertRaises(ValueError):
            RAM(8).cycle(8,0,0)
