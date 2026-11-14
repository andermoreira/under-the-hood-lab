"""Deterministic block storage properties; no disk persistence implied."""
import unittest
from b10_blocks import split_blocks, join_blocks, block_count

class BlockStorageProperties(unittest.TestCase):
    def test_roundtrip_across_boundary_sizes(self):
        for length in (0, 1, 2, 3, 7, 8, 9, 15, 16, 17, 255, 256, 257):
            data = bytes(i % 256 for i in range(length))
            for size in (1, 2, 4, 8, 16, 64, 256):
                with self.subTest(length=length, size=size):
                    chunks = split_blocks(data, size)
                    self.assertEqual(join_blocks(chunks), data)
                    self.assertEqual(len(chunks), block_count(length, size))

    def test_no_block_exceeds_capacity(self):
        data = bytes(range(100))
        for size in range(1, 20):
            blocks = split_blocks(data, size)
            self.assertTrue(all(0 < len(block) <= size for block in blocks))

    def test_invalid_sizes_rejected(self):
        for size in (-100, -1, 0):
            self.assertRaises(ValueError, split_blocks, b"abc", size)
            self.assertRaises(ValueError, block_count, 3, size)

    def test_negative_length_rejected(self):
        self.assertRaises(ValueError, block_count, -1, 4)

    def test_empty_data_has_no_blocks(self):
        self.assertEqual(split_blocks(b"", 512), [])
        self.assertEqual(block_count(0, 512), 0)
        self.assertEqual(join_blocks([]), b"")

if __name__ == "__main__":
    unittest.main()
