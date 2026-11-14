"""Mutation-style controls that must fail when key invariants are violated."""
import unittest
from b05_frames import FrameAllocator
from b06_paging import PAGE_SIZE, translate
from b07_scheduler import schedule
from b09_elf import inspect_header, InvalidELF
from b10_blocks import split_blocks, join_blocks

class NegativeControlTests(unittest.TestCase):
    def test_duplicate_frame_is_detectable(self):
        allocator = FrameAllocator([1, 2])
        observed = [allocator.alloc(), allocator.alloc()]
        mutated = [observed[0], observed[0]]
        self.assertEqual(len(set(observed)), 2)
        self.assertNotEqual(len(set(mutated)), 2)

    def test_wrong_page_offset_is_detectable(self):
        table = {1: (9, True)}
        correct = translate(PAGE_SIZE + 7, table)
        mutated = 9 * PAGE_SIZE
        self.assertEqual(correct, 9 * PAGE_SIZE + 7)
        self.assertNotEqual(correct, mutated)

    def test_unfair_scheduler_trace_is_detectable(self):
        trace = schedule(["A", "B"], 8)
        mutated = ["A"] * 8
        self.assertEqual(abs(trace.count("A") - trace.count("B")), 0)
        self.assertGreater(abs(mutated.count("A") - mutated.count("B")), 1)

    def test_corrupted_elf_magic_is_rejected(self):
        valid = bytes.fromhex("7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00")
        self.assertEqual(inspect_header(valid)["class"], "ELF64")
        corrupted = bytes([0]) + valid[1:]
        self.assertRaises(InvalidELF, inspect_header, corrupted)

    def test_lost_block_is_detectable(self):
        data = b"abcdefghi"
        chunks = split_blocks(data, 4)
        self.assertEqual(join_blocks(chunks), data)
        self.assertNotEqual(join_blocks(chunks[:-1]), data)

if __name__ == "__main__":
    unittest.main()
