"""Contract tests for the test runner itself (no QEMU needed)."""
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "docs" / "pedagogy"))
import run_model_tests as runner

class RunnerContractTests(unittest.TestCase):
    def test_repository_root(self):
        self.assertEqual(runner.ROOT, ROOT)
        self.assertTrue((runner.ROOT / "docs" / "pedagogy" / "examples").is_dir())

    def test_missing_tests_is_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(runner, "EXAMPLES", pathlib.Path(temp)):
                self.assertEqual(runner.main(), 2)

    def test_child_failure_propagates(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            (folder / "test_b_fail.py").write_text(
                "import unittest\n"
                "class Broken(unittest.TestCase):\n"
                " def test_fails(self): self.fail('negative control')\n",
                encoding="utf-8")
            with patch.object(runner, "EXAMPLES", folder):
                self.assertNotEqual(runner.main(), 0)

    def test_child_success_propagates(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            (folder / "test_b_pass.py").write_text(
                "import unittest\n"
                "class Works(unittest.TestCase):\n"
                " def test_passes(self): self.assertTrue(True)\n",
                encoding="utf-8")
            with patch.object(runner, "EXAMPLES", folder):
                self.assertEqual(runner.main(), 0)

if __name__ == "__main__":
    unittest.main()
