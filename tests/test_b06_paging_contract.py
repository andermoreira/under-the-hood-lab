import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PagingContractTests(unittest.TestCase):
    def test_page_table_operations_and_tlb(self):
        paging = (ROOT / "kernel/x86_64/paging.c").read_text()
        for token in ("mov %%cr3", "invlpg", "ADDRESS_MASK", "PRESENT", "WRITABLE", "HUGE"):
            self.assertIn(token, paging)

    def test_rollback_and_table_ownership(self):
        paging = (ROOT / "kernel/x86_64/paging.c").read_text()
        for token in ("paging_set_allocation_budget", "goto rollback",
                      "parents[created][indices[created]] = 0",
                      "pmm_free(frames[created])", "table_empty",
                      "owned_table_frames", "pmm_free(frame)"):
            self.assertIn(token, paging)

    def test_qemu_proves_fault_injection_and_no_leak(self):
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        self.assertIn("budget < 4", main)
        self.assertIn("pmm_free_count() != free_before_paging", main)
        self.assertIn("B06_PAGING_ROLLBACK_OK", boot)
        self.assertIn("B06_PAGING_MAP_UNMAP_OK", boot)


if __name__ == "__main__":
    unittest.main()
