"""Check pedagogical CI actually invokes the consolidated runner."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github" / "workflows" / "pedagogical-model-tests.yml"
RUNNER = ROOT / "docs" / "pedagogy" / "run_model_tests.py"

class GateWiringTests(unittest.TestCase):
    def test_workflow_exists(self):
        self.assertTrue(WORKFLOW.is_file())

    def test_runner_invoked_from_workflow(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("python3 docs/pedagogy/run_model_tests.py", text)

    def test_workflow_has_pull_request_trigger(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("pull_request:", text)

    def test_runner_uses_unittest_and_propagates_exit(self):
        text = RUNNER.read_text(encoding="utf-8")
        self.assertIn('"unittest", "discover"', text)
        self.assertIn("return subprocess.call(command", text)

if __name__ == "__main__":
    unittest.main()
