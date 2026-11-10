import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKBOOKS = ROOT / "docs/workbooks"
TRACK_B = ["B01-TOOLCHAIN", "B02-BOOT-SERIAL", "B03-GDT-IDT", "B04-TIMER-KEYBOARD",
           "B05-PMM", "B06-PAGING-HEAP", "B07-SCHEDULER", "B08-USERMODE",
           "B09-ELF-LOADER", "B10-DISK-FS", "B11-SHELL", "B12-INTEGRATION"]
# PACTO sequence (docs/PEDAGOGY.md) as used by workbooks/A01.md.
SECTIONS = ["Fenômeno", "Previsão", "Analogia", "Onde a analogia falha", "Faça",
            "Refute", "Explique sem analogia", "Transfira", "Revisão", "Evidência"]


class WorkbookStructureTests(unittest.TestCase):
    def test_track_b_follows_pacto_sections(self):
        for name in TRACK_B:
            text = (WORKBOOKS / f"{name}.md").read_text()
            headings = re.findall(r"^## \d+\. (.+)$", text, re.M)
            for section in SECTIONS:
                self.assertTrue(any(h.startswith(section) for h in headings), f"{name}: {section}")
            self.assertIn("<details>", text, f"{name}: gabarito must be hidden")
            for days in ("1 dia", "7 dias", "30 dias"):
                self.assertIn(days, text, f"{name}: spaced review {days}")

    def test_hdl_status_matches_ci_gate(self):
        script = (ROOT / "scripts/test-hdl.sh").read_text()
        gated = set(re.search(r"for test in ([^;]+);", script).group(1).split())
        for name in ("A02", "A03-ADDER", "A03-ALU", "A04-REGISTER", "A05-CPU", "A05-PC"):
            text = (WORKBOOKS / f"{name}.md").read_text()
            self.assertNotRegex(text, r"(HDL|[Ss]imulador oficial)[^.\n]*NOT_RUN", name)
        self.assertTrue({"Add16", "ALU", "Bit", "Register", "CPU", "Mux"} <= gated)

    def test_cpu_jump_bit_comment(self):
        cpu = (ROOT / "hardware/nand2tetris/CPU.hdl").read_text()
        self.assertIn("j1=JLT", cpu)
        self.assertNotIn("j1=JGT", cpu)


if __name__ == "__main__":
    unittest.main()
