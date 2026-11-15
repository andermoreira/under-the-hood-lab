import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_learn_journal import check

class LearnValidatorTests(unittest.TestCase):
    def test_existing_blank_journal_stays_incomplete(self):
        text = (ROOT / "docs/journal/B05.md").read_text()
        result = check(text)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertIn("prediction_missing_or_placeholder", result["findings"])
        self.assertIn("rubric_incomplete_prever", result["findings"])
        self.assertIn("review_incomplete_+30_dias", result["findings"])

    def test_required_sections_and_provenance(self):
        base = (ROOT / "docs/journal/B05.md").read_text()
        findings = check(base)["findings"]
        for number in (1, 2, 5, 6, 7, 10):
            self.assertIn(f"section_{number}_missing_or_placeholder", findings)
        self.assertIn("identity_or_provenance_missing", findings)

    def test_blank_rubric_justification_is_incomplete(self):
        base = (ROOT / "docs/journal/B05.md").read_text()
        base = base.replace("| Prever | ☐ | <...> |", "| Prever | 2 |  |")
        result = check(base)
        self.assertIn("rubric_incomplete_prever", result["findings"])

    def test_missing_review_rows_fail(self):
        result = check("## 3. Prediction\nA\n## 4. Observation\nB\n## 8. Rubric\n## 9. Review\n")
        self.assertIn("review_rows_missing", result["findings"])

    def test_filled_text_is_not_automatically_pass(self):
        # Even complete text is only READY_FOR_HUMAN_REVIEW, never PASS.
        base = (ROOT / "docs/journal/B05.md").read_text()
        base = base.replace("<...>", "explicação própria")
        base = base.replace("$ <comando>", "$ make test").replace("<comando>", "make test")
        base = base.replace("<saída>", "exit=0").replace("<hash>", "abc1234")
        for dimension in ("Prever", "Construir", "Explicar", "Refutar", "Transferir"):
            base = base.replace("| " + dimension + " | ☐ |", "| " + dimension + " | 2 |")
        base = base.replace("| — | — |", "| 2026-12-01 | recuperação própria |")
        self.assertNotEqual(check(base)["status"], "PASS")

if __name__ == "__main__":
    unittest.main()
