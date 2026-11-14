import unittest
from b12_capstone import assess,REQUIRED,IncompleteEvidence
class Tests(unittest.TestCase):
    def test_complete(self): self.assertTrue(assess({key:True for key in REQUIRED}))
    def test_missing_reboot(self):
        e={key:True for key in REQUIRED};e["reboot"]=False
        self.assertRaises(IncompleteEvidence,assess,e)
    def test_missing_readback(self):
        e={key:True for key in REQUIRED};e.pop("readback")
        self.assertRaises(IncompleteEvidence,assess,e)
    def test_string_not_pass(self):
        e={key:True for key in REQUIRED};e["isolation"]="PASS"
        self.assertRaises(IncompleteEvidence,assess,e)
    def test_wrong_type(self): self.assertRaises(TypeError,assess,[])
if __name__=="__main__": unittest.main()
