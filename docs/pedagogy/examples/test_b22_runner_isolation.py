"""Runner should discover tests in a sandbox and preserve failures."""
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "docs" / "pedagogy"))
import run_model_tests as runner

class RunnerIsolationTests(unittest.TestCase):
    def _run(self, filename, body):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / filename).write_text(body, encoding="utf-8")
            with patch.object(runner, "EXAMPLES", root):
                return runner.main()

    def test_syntax_error_is_not_green(self):
        self.assertNotEqual(self._run("test_b_syntax.py", "def broken(:\n pass\n"), 0)

    def test_import_error_is_not_green(self):
        self.assertNotEqual(self._run("test_b_import.py", "import module_that_does_not_exist_8392\n"), 0)

    def test_failing_assertion_is_not_green(self):
        body = "import unittest\nclass T(unittest.TestCase):\n def test_fail(self): self.assertEqual(1, 2)\n"
        self.assertNotEqual(self._run("test_b_assert.py", body), 0)

    def test_unrelated_file_does_not_count_as_test(self):
        self.assertEqual(self._run("example.py", "print('not a test')\n"), 2)

    def test_valid_unittest_is_green(self):
        body = "import unittest\nclass T(unittest.TestCase):\n def test_pass(self): self.assertEqual(1, 1)\n"
        self.assertEqual(self._run("test_b_pass.py", body), 0)

if __name__ == "__main__":
    unittest.main()
