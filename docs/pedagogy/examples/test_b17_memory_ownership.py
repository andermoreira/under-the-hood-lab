"""Frame ownership and exhaustion invariants under repeated allocation cycles."""
import unittest
from b05_frames import FrameAllocator, OutOfFrames

class FrameOwnershipProperties(unittest.TestCase):
    def test_no_frame_returned_twice_while_allocated(self):
        a = FrameAllocator(range(16))
        values = [a.alloc() for _ in range(16)]
        self.assertEqual(values, list(range(16)))
        self.assertEqual(len(set(values)), 16)
        self.assertRaises(OutOfFrames, a.alloc)

    def test_release_then_reallocate_preserves_ownership(self):
        a = FrameAllocator([2, 4, 6])
        self.assertEqual([a.alloc() for _ in range(3)], [2, 4, 6])
        a.release(4)
        self.assertEqual(a.alloc(), 4)
        self.assertRaises(ValueError, a.release, 99)

    def test_double_free_rejected_after_many_cycles(self):
        a = FrameAllocator([5])
        for _ in range(50):
            self.assertEqual(a.alloc(), 5)
            a.release(5)
            self.assertRaises(ValueError, a.release, 5)

    def test_reserved_frames_are_never_allocated(self):
        allowed = {3, 7, 11}
        a = FrameAllocator(allowed)
        self.assertEqual({a.alloc() for _ in range(3)}, allowed)
        self.assertRaises(OutOfFrames, a.alloc)

    def test_empty_allocator_is_consistently_exhausted(self):
        a = FrameAllocator([])
        for _ in range(3):
            self.assertRaises(OutOfFrames, a.alloc)

if __name__ == "__main__":
    unittest.main()
