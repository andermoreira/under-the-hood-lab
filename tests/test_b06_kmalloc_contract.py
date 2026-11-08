import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class KmallocContractTests(unittest.TestCase):
    def test_size_classes_over_page_heap(self):
        code = (ROOT / "kernel/x86_64/kmalloc.c").read_text()
        for token in ("void *kmalloc(size_t size)", "int kfree(void *pointer)",
                      "heap_alloc_page()", "SLAB_MAGIC", "MAX_OBJECT 1024"):
            self.assertIn(token, code)
        self.assertIn("kmalloc.o", (ROOT / "scripts/build-kernel.sh").read_text())

    def test_qemu_gate_covers_reuse_and_invalid_free(self):
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        self.assertIn("B06_KMALLOC_OK", boot)
        for token in ("kfree(a)", "kmalloc(0)", "kmalloc(1025)", "free_before_kmalloc"):
            self.assertIn(token, main)


if __name__ == "__main__":
    unittest.main()
