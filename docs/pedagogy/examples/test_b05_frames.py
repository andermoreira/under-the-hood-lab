import unittest
from b05_frames import FrameAllocator,OutOfFrames
class Tests(unittest.TestCase):
    def test_first_fit(self):
        a=FrameAllocator([7,2,5]);self.assertEqual(a.alloc(),2);self.assertEqual(a.alloc(),5)
    def test_exhaustion(self):
        a=FrameAllocator([]);self.assertRaises(OutOfFrames,a.alloc)
    def test_release_reuse(self):
        a=FrameAllocator([3]);self.assertEqual(a.alloc(),3);a.release(3);self.assertEqual(a.alloc(),3)
    def test_double_free(self):
        a=FrameAllocator([3]);a.alloc();a.release(3);self.assertRaises(ValueError,a.release,3)
    def test_reserved_not_allocated(self):
        a=FrameAllocator([1,4]);self.assertNotIn(a.alloc(),{0,2,3})
if __name__=="__main__": unittest.main()
