import unittest
from b08_syscalls import dispatch,SyscallError
class Tests(unittest.TestCase):
    def test_read(self): self.assertEqual(dispatch(1,1,b"ABC"),66)
    def test_exit(self): self.assertEqual(dispatch(2,0,b""),0)
    def test_unknown(self): self.assertRaises(SyscallError,dispatch,99,0,b"")
    def test_out_of_bounds(self): self.assertRaises(SyscallError,dispatch,1,3,b"ABC")
    def test_negative_pointer(self): self.assertRaises(SyscallError,dispatch,1,-1,b"ABC")
    def test_invalid_exit(self): self.assertRaises(SyscallError,dispatch,2,256,b"")
if __name__=="__main__": unittest.main()
