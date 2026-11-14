"""Realistic ELF ident checks with known byte arrays, not shared model constants."""
import unittest
from b09_elf import InvalidELF, inspect_header

class ElfIdentifierBoundaryTests(unittest.TestCase):
    def test_genuine_elf64_le_ident(self):
        # 7f E L F, ELFCLASS64=2, ELFDATA2LSB=1, EV_CURRENT=1
        header = bytes.fromhex("7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00")
        self.assertEqual(inspect_header(header), {"class": "ELF64", "endian": "little"})

    def test_printable_backslash_is_not_magic(self):
        # Regression: literal backslash-x-7-f is not byte 0x7f.
        wrong = b"\\x7fELF" + bytes([2, 1, 1]) + bytes(9)
        self.assertRaises(InvalidELF, inspect_header, wrong)

    def test_all_truncations_rejected(self):
        valid = bytes.fromhex("7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00")
        for length in range(16):
            with self.subTest(length=length):
                self.assertRaises(InvalidELF, inspect_header, valid[:length])

    def test_invalid_class_and_encoding(self):
        valid = bytearray(bytes.fromhex("7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00"))
        for index, value in ((4, 1), (5, 2), (6, 0)):
            wrong = bytearray(valid)
            wrong[index] = value
            with self.subTest(index=index):
                self.assertRaises(InvalidELF, inspect_header, bytes(wrong))

if __name__ == "__main__":
    unittest.main()
