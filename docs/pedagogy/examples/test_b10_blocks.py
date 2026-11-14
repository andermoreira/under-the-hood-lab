import unittest
from b10_blocks import split_blocks,join_blocks,block_count
class Tests(unittest.TestCase):
    def test_ten_bytes(self): self.assertEqual(split_blocks(b"abcdefghij",4),[b"abcd",b"efgh",b"ij"])
    def test_roundtrip(self): self.assertEqual(join_blocks(split_blocks(b"abcde",2)),b"abcde")
    def test_empty(self): self.assertEqual(split_blocks(b"",4),[])
    def test_count(self): self.assertEqual(block_count(10,4),3)
    def test_invalid(self): self.assertRaises(ValueError,split_blocks,b"abc",0)
if __name__=="__main__": unittest.main()
