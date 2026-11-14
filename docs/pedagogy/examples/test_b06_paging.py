"""Execute: python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b06_paging.py' -v"""
import unittest
from b06_paging import PAGE_SIZE, PageFault, translate, write_address

class PagingTests(unittest.TestCase):
    def setUp(self):
        self.table = {2: (7, False), 3: (9, True)}

    def test_offset_preserved(self):
        self.assertEqual(translate(0x2005, self.table), 7 * PAGE_SIZE + 5)

    def test_page_boundary(self):
        self.assertEqual(translate(0x3000, self.table), 9 * PAGE_SIZE)

    def test_unmapped_fault(self):
        with self.assertRaises(PageFault):
            translate(0x1000, self.table)

    def test_readonly_write_fault(self):
        with self.assertRaises(PageFault):
            write_address(0x2005, self.table)

    def test_writable_page(self):
        self.assertEqual(write_address(0x3000, self.table), 9 * PAGE_SIZE)

    def test_negative_address(self):
        with self.assertRaises(ValueError):
            translate(-1, self.table)

if __name__ == "__main__":
    unittest.main()
