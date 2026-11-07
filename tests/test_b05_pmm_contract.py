import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class PmmContractTests(unittest.TestCase):
    def test_only_usable_memory_is_released_to_allocator(self):
        code = (ROOT / "kernel/x86_64/pmm.c").read_text()
        self.assertIn("LIMINE_MEMMAP_USABLE", code)
        self.assertIn("MAX_FRAMES", code)
        self.assertIn("owned[", code)
        self.assertIn("if (!physical || physical % PAGE_SIZE", code)
    def test_boot_smoke_is_mandatory(self):
        self.assertIn("B05_PMM_ALLOC_FREE_OK", (ROOT / "scripts/test-kernel-boot.sh").read_text())
        self.assertIn("pmm_free(first)", (ROOT / "kernel/x86_64/main.c").read_text())
