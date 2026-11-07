import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class BootContractTests(unittest.TestCase):
    def test_serial_marker_is_emitted_after_protocol_check(self):
        source = (ROOT / "kernel/x86_64/main.c").read_text()
        self.assertIn('serial_write("KERNEL_READY\\n")', source)
        self.assertLess(source.index("LIMINE_BASE_REVISION_SUPPORTED"), source.index('serial_write("KERNEL_READY'))

    def test_boot_gate_checks_actual_qemu_output(self):
        script = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        for token in ("qemu-system-x86_64", "timeout", "serial.log", "grep -Fxq 'KERNEL_READY'", "limine bios-install"):
            self.assertIn(token, script)
        self.assertIn("rc != 124", script)

    def test_ci_runs_boot_gate(self):
        workflow = (ROOT / ".github/workflows/tests.yml").read_text()
        self.assertIn("make test-kernel-boot", workflow)
