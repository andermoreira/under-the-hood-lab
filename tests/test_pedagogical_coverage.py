"""Structural safeguards only: human review remains required for pedagogical depth."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOUNDATIONS = ROOT / "docs" / "foundations"
WORKBOOKS = ROOT / "docs" / "workbooks"
F = ["F01-BITS-BYTES", "F02-LOGICA", "F03-PORTAS-CIRCUITOS",
     "F04-ESTADO-CPU", "F05-CODIGO-MAQUINA", "F06-ENDERECOS-MEMORIA",
     "F07-BOOT", "F08-SISTEMA-OPERACIONAL"]
A = ["A01", "A02", "A03-ADDER", "A03-ALU", "A04-REGISTER",
     "A05-CPU", "A05-PC"]
B = ["B01-TOOLCHAIN", "B02-BOOT-SERIAL", "B03-GDT-IDT",
     "B04-TIMER-KEYBOARD", "B05-PMM", "B06-PAGING-HEAP",
     "B07-SCHEDULER", "B08-USERMODE", "B09-ELF-LOADER",
     "B10-DISK-FS", "B11-SHELL", "B12-INTEGRATION"]


class PedagogicalCoverage(unittest.TestCase):
    def test_expected_lessons_exist(self):
        for name in F:
            with self.subTest(name=name):
                self.assertTrue((FOUNDATIONS / f"{name}.md").is_file())
        for name in A + B:
            with self.subTest(name=name):
                self.assertTrue((WORKBOOKS / f"{name}.md").is_file())

    def test_mermaid_and_limits(self):
        for path in [*(FOUNDATIONS / f"{n}.md" for n in F),
                     *(WORKBOOKS / f"{n}.md" for n in A + B)]:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertEqual(text.count("```mermaid"), 1)
                self.assertIn("flowchart ", text)
                self.assertTrue(
                    any(term in text.lower() for term in
                        ("onde a analogia", "onde falha", "limite")),
                    "Missing limitation of analogy"
                )
                self.assertTrue(
                    any(term in text.lower() for term in
                        ("exemplo resolvido", "exemplo", "experimento")),
                    "Missing worked example or experiment"
                )

    def test_mermaid_fences_closed(self):
        for path in [*(FOUNDATIONS / f"{n}.md" for n in F),
                     *(WORKBOOKS / f"{n}.md" for n in A + B)]:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertEqual(len(re.findall(r"^```", text, re.M)) % 2, 0)

    def test_no_false_verification_claim_in_foundations(self):
        for name in F:
            with self.subTest(name=name):
                text = (FOUNDATIONS / f"{name}.md").read_text(encoding="utf-8")
                self.assertIn("NOT_RUN", text)


if __name__ == "__main__":
    unittest.main()
