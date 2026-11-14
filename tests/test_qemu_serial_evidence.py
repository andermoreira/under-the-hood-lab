import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from verify_qemu_serial import REQUIRED, assess_serial

class QemuSerialEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.valid = "\n".join(REQUIRED) + "\n"

    def test_complete_serial_evidence(self):
        self.assertEqual(assess_serial(self.valid)["status"], "PASS")

    def test_each_missing_marker_fails(self):
        for marker in REQUIRED:
            with self.subTest(marker=marker):
                text = "\n".join(x for x in REQUIRED if x != marker)
                self.assertIn(marker, assess_serial(text)["missing"])

    def test_substring_does_not_count(self):
        text = self.valid.replace("B05_PMM_ALLOC_FREE_OK", "PREFIX_B05_PMM_ALLOC_FREE_OK")
        self.assertEqual(assess_serial(text)["status"], "FAIL")

    def test_boot_marker_must_precede_milestones(self):
        text = "\n".join(REQUIRED[1:]) + "\nKERNEL_READY\n"
        self.assertFalse(assess_serial(text)["boot_before_milestones"])

    def test_panic_marker_fails(self):
        self.assertEqual(assess_serial(self.valid + "PANIC: fatal\n")["status"], "FAIL")

    def test_cli_missing_log_is_nonzero(self):
        with tempfile.TemporaryDirectory() as directory:
            process = subprocess.run([sys.executable, str(ROOT / "tools/verify_qemu_serial.py"),
                                      str(Path(directory) / "absent.log")], capture_output=True)
            self.assertNotEqual(process.returncode, 0)

if __name__ == "__main__":
    unittest.main()
