"""Contract tests for the actual QEMU boot smoke harness.

These are static safety checks, not a substitute for running QEMU.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "test-kernel-boot.sh"

class BootHarnessContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")

    def test_qemu_invocation_is_real(self):
        self.assertIn("qemu-system-x86_64", self.script)
        self.assertIn('-serial "file:$OUT/serial.log"', self.script)
        self.assertIn('-no-reboot', self.script)

    def test_timeout_is_bounded(self):
        self.assertIn("timeout --signal=TERM --kill-after=3s 20s", self.script)

    def test_pmm_and_paging_are_mandatory(self):
        for marker in ("B05_PMM_ALLOC_FREE_OK", "B06_PAGING_MAP_UNMAP_OK",
                       "B06_PAGING_ROLLBACK_OK"):
            with self.subTest(marker=marker):
                self.assertIn("grep -Fxq '" + marker + "'", self.script)

    def test_boot_and_crash_containment_are_mandatory(self):
        for marker in ("KERNEL_READY", "B12_CRASH_CONTAINED"):
            self.assertIn("grep -Fxq '" + marker + "'", self.script)

    def test_unexpected_fatal_faults_rejected(self):
        self.assertIn("EXCEPTION_PF_(CR2|ERROR)_", self.script)
        self.assertIn("PANIC|KERNEL_FAULT", self.script)

if __name__ == "__main__":
    unittest.main()
