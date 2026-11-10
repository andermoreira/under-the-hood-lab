import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class IntegrationContractTests(unittest.TestCase):
    def test_page_fault_handler_distinguishes_ring3(self):
        asm = (ROOT / "kernel/x86_64/interrupts.S").read_text()
        c = (ROOT / "kernel/x86_64/interrupts.c").read_text()
        # The ISR must pass the saved CS so the handler can read CPL.
        self.assertIn("16(%rsp), %rsi", asm)
        self.assertIn("exception_page_fault(uint64_t error_code, uint64_t saved_cs)", c)
        self.assertIn("(saved_cs & 3) == 3", c)
        self.assertIn("usermode_return", c)

    def test_usermode_tracks_active_task_for_containment(self):
        um = (ROOT / "kernel/x86_64/usermode.c").read_text()
        self.assertIn("usermode_fault_return_rsp", um)
        self.assertIn("USER_EXIT_FAULT", um)
        self.assertIn("user_active", um)

    def test_crash_program_is_built_and_embedded(self):
        build = (ROOT / "scripts/build-kernel.sh").read_text()
        self.assertIn("crash.elf", build)
        self.assertIn("CRASH_ELF_PATH", build)
        self.assertIn("crash_elf.o", build)

    def test_boot_gate_proves_containment_and_survival(self):
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        # The crash program must reach ring 3, fault, be contained, and the
        # shell must keep running afterwards.
        self.assertIn("B12_CRASH_BEFORE_FAULT", boot)
        self.assertIn("B12_CRASH_CONTAINED", boot)
        self.assertIn("B11_SHELL_OK", boot)
        # A fatal #PF (ring 0) is still rejected; only user PF is tolerated.
        self.assertIn("EXCEPTION_PF_(CR2|ERROR)_", boot)

    def test_two_distinct_user_programs_exist(self):
        # "Definição de utilizável": run two of our own user programs.
        hello = (ROOT / "kernel/x86_64/userland/hello.S").read_text()
        crash = (ROOT / "kernel/x86_64/userland/crash.S").read_text()
        self.assertIn("B09_ELF_HELLO", hello)
        self.assertIn("B12_CRASH_BEFORE_FAULT", crash)


if __name__ == "__main__":
    unittest.main()
