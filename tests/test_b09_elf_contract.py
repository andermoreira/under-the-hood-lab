import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ElfLoaderContractTests(unittest.TestCase):
    def test_loader_validates_header_fields(self):
        code = (ROOT / "kernel/x86_64/elf.c").read_text()
        # Magic, class, endianness, type and machine must all be checked.
        self.assertIn("0x7f", code)
        self.assertIn("ELFCLASS64", code)
        self.assertIn("ELF_ET_EXEC", code)
        self.assertIn("ELF_EM_X86_64", code)
        self.assertIn("PT_LOAD", code)
        # Segments are mapped as user pages and filesz<=memsz is enforced.
        self.assertIn("paging_map_user_page", code)
        self.assertIn("p_filesz > ph->p_memsz", code)

    def test_user_program_is_built_and_embedded(self):
        build = (ROOT / "scripts/build-kernel.sh").read_text()
        self.assertIn("hello.elf", build)
        self.assertIn("USER_ELF_PATH", build)
        self.assertIn("user_elf.o", build)
        embed = (ROOT / "kernel/x86_64/userland/embed.S").read_text()
        self.assertIn(".incbin USER_ELF_PATH", embed)
        self.assertIn("user_elf_start", embed)

    def test_nxe_is_preserved_when_enabling_syscall(self):
        # Regression guard for the reserved-bit #PF: enabling SCE must keep NXE,
        # and EFER must be read as EDX:EAX (not the "=A" that drops the high
        # dword).
        um = (ROOT / "kernel/x86_64/usermode.c").read_text()
        self.assertIn("EFER_NXE", um)
        self.assertIn("EFER_SCE | EFER_NXE", um)
        self.assertIn('"=a"(lo), "=d"(hi)', um)
        self.assertNotIn('"=A"(efer)', um)

    def test_boot_gate_runs_loaded_program_in_ring3(self):
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        build = (ROOT / "scripts/build-kernel.sh").read_text()
        self.assertIn("B09_ELF_HELLO", boot)
        self.assertIn("B09_ELF_OK", boot)
        self.assertIn("elf_loader_selftest", main)
        self.assertIn("elf.o", build)

    def test_bootloader_tables_are_protected_in_pmm(self):
        # Hardening for review finding kernel #4: the live higher-half tables
        # are reserved so the PMM never allocates over them.
        pmm = (ROOT / "kernel/x86_64/pmm.c").read_text()
        paging = (ROOT / "kernel/x86_64/paging.c").read_text()
        self.assertIn("int pmm_reserve(uint64_t physical)", pmm)
        self.assertIn("reserve_table_frames", paging)


if __name__ == "__main__":
    unittest.main()
