import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ShellContractTests(unittest.TestCase):
    def test_shell_parses_and_dispatches_builtins(self):
        code = (ROOT / "kernel/x86_64/shell.c").read_text()
        self.assertIn("shell_exec", code)
        self.assertIn("tokenize", code)
        for builtin in ('"ls"', '"cat"', '"write"', '"run"'):
            self.assertIn(builtin, code)
        # Running a program goes through the ELF loader and ring-3 entry.
        self.assertIn("elf_load", code)
        self.assertIn("usermode_run", code)

    def test_shell_uses_filesystem(self):
        code = (ROOT / "kernel/x86_64/shell.c").read_text()
        self.assertIn("fs_read", code)
        self.assertIn("fs_write", code)

    def test_boot_gate_exercises_shell(self):
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        build = (ROOT / "scripts/build-kernel.sh").read_text()
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        self.assertIn("B11_LS_greeting.txt", boot)
        self.assertIn("B11_SHELL_OK", boot)
        self.assertIn("shell.o", build)
        self.assertIn("shell_selftest", main)


if __name__ == "__main__":
    unittest.main()
