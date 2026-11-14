import unittest
from b07_scheduler import schedule,schedule_ready
class Tests(unittest.TestCase):
    def test_rotation(self): self.assertEqual(schedule(["A","B","C"],7),["A","B","C","A","B","C","A"])
    def test_blocked(self): self.assertEqual(schedule_ready(["A","B","C"],{"B"},4),["A","C","A","C"])
    def test_empty(self): self.assertEqual(schedule([],4),[])
    def test_duplicate(self): self.assertRaises(ValueError,schedule,["A","A"],2)
    def test_negative_ticks(self): self.assertRaises(ValueError,schedule,["A"],-1)
if __name__=="__main__": unittest.main()
