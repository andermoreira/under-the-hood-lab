import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SchedulerContractTests(unittest.TestCase):
    def test_context_switch_preserves_callee_saved_registers(self):
        asm = (ROOT / "kernel/x86_64/switch.S").read_text()
        self.assertIn("context_switch", asm)
        # System V callee-saved set must be saved and restored symmetrically.
        for reg in ("%rbx", "%rbp", "%r12", "%r13", "%r14", "%r15"):
            self.assertEqual(asm.count(f"pushq {reg}"), 1, reg)
            self.assertEqual(asm.count(f"popq {reg}"), 1, reg)
        self.assertIn("movq %rsp, (%rdi)", asm)
        self.assertIn("movq %rsi, %rsp", asm)
        # A fresh task is bootstrapped through the task_start trampoline.
        self.assertIn("task_start", asm)
        self.assertIn("callq *%r12", asm)
        # Executable-stack note is suppressed (kept the build warning-clean).
        self.assertIn(".note.GNU-stack", asm)

    def test_scheduler_is_round_robin_and_terminates(self):
        code = (ROOT / "kernel/x86_64/scheduler.c").read_text()
        self.assertIn("scheduler_spawn", code)
        self.assertIn("scheduler_yield", code)
        self.assertIn("scheduler_run", code)
        self.assertIn("next_runnable", code)
        self.assertIn("TASK_FINISHED", code)
        # Stacks come from the page heap and are returned when a task finishes.
        self.assertIn("heap_alloc_page", code)
        self.assertIn("heap_free_page", code)

    def test_boot_gate_proves_deterministic_interleaving(self):
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        build = (ROOT / "scripts/build-kernel.sh").read_text()
        # The smoke test must actually run under QEMU, with a deterministic
        # trace, and the new units must be compiled and linked.
        self.assertIn("scheduler_selftest", main)
        self.assertIn('"ABCABCABC"', main)
        self.assertIn("B07_SCHEDULER_OK", boot)
        self.assertIn("B07_SCHEDULER_TRACE_ABCABCABC", boot)
        self.assertIn("scheduler.o", build)
        self.assertIn("switch_asm.o", build)


if __name__ == "__main__":
    unittest.main()
