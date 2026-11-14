"""Boundary tests for the didactic syscall dispatcher, not a kernel gate."""
import unittest
from b08_syscalls import dispatch, SyscallError

class SyscallBoundaryTests(unittest.TestCase):
    def test_every_valid_byte_offset(self):
        memory = bytes(range(256))
        for offset in range(len(memory)):
            with self.subTest(offset=offset):
                self.assertEqual(dispatch(1, offset, memory), offset)

    def test_first_out_of_bounds_and_empty_memory(self):
        self.assertRaises(SyscallError, dispatch, 1, 1, b"x")
        self.assertRaises(SyscallError, dispatch, 1, 0, b"")

    def test_exit_code_full_byte_range(self):
        for code in range(256):
            with self.subTest(code=code):
                self.assertEqual(dispatch(2, code, b""), code)
        self.assertRaises(SyscallError, dispatch, 2, 256, b"")

    def test_unknown_syscall_never_accepted(self):
        for number in (-1, 0, 3, 999, "1"):
            with self.subTest(number=number):
                self.assertRaises(SyscallError, dispatch, number, 0, b"a")

    def test_negative_arguments_rejected(self):
        for number in (1, 2):
            self.assertRaises(SyscallError, dispatch, number, -1, b"a")

if __name__ == "__main__":
    unittest.main()
