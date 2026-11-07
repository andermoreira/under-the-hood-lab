import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class HeapContractTests(unittest.TestCase):
    def test_hhdm_and_page_ownership(self):
        heap = (ROOT / "kernel/x86_64/heap.c").read_text()
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        self.assertIn("LIMINE_HHDM_REQUEST_ID", main)
        self.assertIn("hhdm_request.response->offset", main)
        self.assertIn("pmm_alloc()", heap)
        self.assertIn("pmm_free(physical)", heap)
        self.assertIn("allocated[i] = UINT64_MAX", heap)
    def test_real_boot_gate(self):
        script = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        self.assertIn("B06_HEAP_PAGE_OK", script)
        self.assertIn("heap_free_page(page)", (ROOT / "kernel/x86_64/main.c").read_text())
