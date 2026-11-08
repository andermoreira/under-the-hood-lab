import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AddressSpaceContractTests(unittest.TestCase):
    def test_kernel_builds_and_loads_its_own_pml4(self):
        paging = (ROOT / "kernel/x86_64/paging.c").read_text()
        self.assertIn("int paging_adopt_kernel_space(void)", paging)
        self.assertIn("mov %0, %%cr3", paging)
        # Only the higher half (entries 256..511) is shared with Limine.
        self.assertIn("for (unsigned i = 256; i < 512; ++i)", paging)

    def test_qemu_gate_requires_own_pml4_before_paging_tests(self):
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        self.assertIn("B06_OWN_PML4_OK", boot)
        self.assertLess(main.index("paging_adopt_kernel_space()"),
                        main.index("paging_set_allocation_budget(budget)"))

    def test_pmm_hot_path_does_not_log(self):
        pmm = (ROOT / "kernel/x86_64/pmm.c").read_text()
        body = re.search(r"uint64_t pmm_alloc\(void\) \{(.*?)\n\}", pmm, re.S).group(1)
        self.assertNotIn("serial_write", body)


if __name__ == "__main__":
    unittest.main()
