"""Paging boundary invariants; models virtual-to-physical translation only."""
import unittest
from b06_paging import PAGE_SIZE, PageFault, translate, write_address

class PagingBoundaryTests(unittest.TestCase):
    def test_boundary_between_two_pages(self):
        table = {2: (7, True), 3: (9, True)}
        self.assertEqual(translate(3 * PAGE_SIZE - 1, table), 8 * PAGE_SIZE - 1)
        self.assertEqual(translate(3 * PAGE_SIZE, table), 9 * PAGE_SIZE)

    def test_every_offset_in_page(self):
        table = {4: (20, True)}
        for offset in range(PAGE_SIZE):
            self.assertEqual(translate(4 * PAGE_SIZE + offset, table), 20 * PAGE_SIZE + offset)

    def test_read_only_page_can_be_read_but_not_written(self):
        table = {0: (2, False)}
        self.assertEqual(translate(123, table), 2 * PAGE_SIZE + 123)
        self.assertRaises(PageFault, write_address, 123, table)

    def test_unmapped_page_faults(self):
        table = {1: (4, True)}
        for address in (0, 2 * PAGE_SIZE, 9 * PAGE_SIZE):
            with self.subTest(address=address):
                self.assertRaises(PageFault, translate, address, table)

    def test_negative_address_and_frame_rejected(self):
        self.assertRaises(ValueError, translate, -1, {0: (0, True)})
        self.assertRaises(ValueError, translate, 0, {0: (-1, True)})

if __name__ == "__main__":
    unittest.main()
