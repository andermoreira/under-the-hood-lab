"""Boundary invariants independent from the original model fixtures."""
import unittest
from b05_frames import FrameAllocator, OutOfFrames
from b06_paging import PAGE_SIZE, PageFault, translate, write_address
from b07_scheduler import schedule
from b08_syscalls import SyscallError, dispatch
from b10_blocks import split_blocks, join_blocks, block_count
from b11_shell import CommandError, parse
from b12_capstone import IncompleteEvidence, REQUIRED, assess

class CrossModuleBoundaryTests(unittest.TestCase):
    def test_allocator_never_duplicates_active_frame(self):
        a = FrameAllocator(range(8))
        allocated = [a.alloc() for _ in range(8)]
        self.assertEqual(len(set(allocated)), 8)
        self.assertRaises(OutOfFrames, a.alloc)

    def test_paging_preserves_every_offset_on_one_page(self):
        table = {4: (12, True)}
        for offset in range(PAGE_SIZE):
            self.assertEqual(translate(4 * PAGE_SIZE + offset, table),
                             12 * PAGE_SIZE + offset)

    def test_paging_readonly_is_readable_not_writable(self):
        table = {1: (9, False)}
        self.assertEqual(translate(PAGE_SIZE, table), 9 * PAGE_SIZE)
        self.assertRaises(PageFault, write_address, PAGE_SIZE, table)

    def test_scheduler_trace_never_introduces_unknown_task(self):
        tasks = ["alpha", "beta", "gamma"]
        trace = schedule(tasks, 101)
        self.assertEqual(len(trace), 101)
        self.assertEqual(set(trace), set(tasks))

    def test_syscall_rejects_negative_and_oob_pointers(self):
        for address in (-1, 3, 999):
            with self.subTest(address=address):
                self.assertRaises(SyscallError, dispatch, 1, address, b"abc")

    def test_blocks_roundtrip_for_small_sizes(self):
        for length in range(33):
            for size in range(1, 9):
                data = bytes(range(length))
                self.assertEqual(join_blocks(split_blocks(data, size)), data)
                self.assertEqual(len(split_blocks(data, size)), block_count(length, size))

    def test_shell_never_dispatches_unknown_commands(self):
        for command in ("sudo", "rm", "unknown", "HELP"):
            with self.subTest(command=command):
                self.assertRaises(CommandError, parse, command)

    def test_capstone_requires_real_boolean_true(self):
        for replacement in ("PASS", 1, None, False):
            evidence = {key: True for key in REQUIRED}
            evidence["readback"] = replacement
            with self.subTest(replacement=replacement):
                self.assertRaises(IncompleteEvidence, assess, evidence)

if __name__ == "__main__":
    unittest.main()
