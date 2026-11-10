import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class UsermodeContractTests(unittest.TestCase):
    def test_gdt_has_ring3_selectors_and_tss(self):
        code = (ROOT / "kernel/x86_64/interrupts.c").read_text()
        # Ring-3 code/data descriptors and a TSS selector must exist.
        self.assertIn("ring-3 data, selector 0x38", code)
        self.assertIn("ring-3 64-bit code, selector 0x40", code)
        self.assertIn("TSS_SELECTOR", code)
        self.assertIn("ltr", code)
        self.assertIn("tss_set_kernel_stack", code)

    def test_syscall_msrs_and_abi(self):
        code = (ROOT / "kernel/x86_64/usermode.c").read_text()
        for msr in ("MSR_EFER", "MSR_STAR", "MSR_LSTAR", "MSR_SFMASK"):
            self.assertIn(msr, code)
        self.assertIn("EFER_SCE", code)
        # STAR layout: SYSRET base 0x30, SYSCALL base 0x28.
        self.assertIn("(uint64_t)0x30 << 48", code)
        self.assertIn("(uint64_t)0x28 << 32", code)
        self.assertIn("syscall_dispatch", code)
        self.assertIn("SYS_write", code)
        self.assertIn("SYS_exit", code)

    def test_ring3_entry_uses_sysret_and_clears_registers(self):
        asm = (ROOT / "kernel/x86_64/usermode.S").read_text()
        self.assertIn("sysretq", asm)
        self.assertIn("usermode_enter", asm)
        self.assertIn("syscall_entry", asm)
        # Entry to ring 3 must not leak kernel register contents.
        self.assertIn("xorl %eax, %eax", asm)

    def test_user_page_mapping_sets_user_bit(self):
        paging = (ROOT / "kernel/x86_64/paging.c").read_text()
        self.assertIn("paging_map_user_page", paging)
        self.assertIn("#define USER", paging)
        self.assertIn("PRESENT | WRITABLE | USER", paging)

    def test_boot_gate_proves_ring3_roundtrip(self):
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        build = (ROOT / "scripts/build-kernel.sh").read_text()
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        self.assertIn("B08_USERLAND_HELLO", boot)
        self.assertIn("B08_USERMODE_OK", boot)
        self.assertIn("usermode.o", build)
        self.assertIn("usermode_asm.o", build)
        self.assertIn("userprog_asm.o", build)
        self.assertIn("usermode_selftest", main)


if __name__ == "__main__":
    unittest.main()
