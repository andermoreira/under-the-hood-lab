import unittest
from b09_elf import inspect_header,InvalidELF
VALID=b"\\x7fELF"+bytes([2,1,1])+bytes(9)
class Tests(unittest.TestCase):
    def test_valid_ident(self): self.assertEqual(inspect_header(VALID)["class"],"ELF64")
    def test_real_elf_magic_bytes(self):
        self.assertEqual(VALID[:4], bytes([127, 69, 76, 70]))

    def test_truncated_header_15_bytes(self):
        self.assertRaises(InvalidELF, inspect_header, VALID[:15])

    def test_short(self): self.assertRaises(InvalidELF,inspect_header,b"ELF")
    def test_magic(self): self.assertRaises(InvalidELF,inspect_header,b"NOPE"+VALID[4:])
    def test_elf32(self): self.assertRaises(InvalidELF,inspect_header,VALID[:4]+bytes([1])+VALID[5:])
    def test_big_endian(self): self.assertRaises(InvalidELF,inspect_header,VALID[:5]+bytes([2])+VALID[6:])
    def test_version(self): self.assertRaises(InvalidELF,inspect_header,VALID[:6]+bytes([0])+VALID[7:])
if __name__=="__main__": unittest.main()
