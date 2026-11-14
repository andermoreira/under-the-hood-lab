"""Guard against silently shrinking the pedagogical regression suite."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "docs" / "pedagogy" / "examples"
REQUIRED = (
    "test_b05_frames.py",
    "test_b06_paging.py",
    "test_b07_scheduler.py",
    "test_b08_syscalls.py",
    "test_b09_elf.py",
    "test_b10_blocks.py",
    "test_b11_shell.py",
    "test_b12_capstone.py",
)

class DiscoveryRegressionTests(unittest.TestCase):
    def test_foundation_modules_present(self):
        missing = [name for name in REQUIRED if not (EXAMPLES / name).is_file()]
        self.assertEqual(missing, [], f"missing foundational tests: {missing}")

    def test_each_foundation_module_has_discoverable_tests(self):
        loader = unittest.TestLoader()
        for name in REQUIRED:
            with self.subTest(name=name):
                suite = loader.discover(str(EXAMPLES), pattern=name)
                self.assertGreater(suite.countTestCases(), 0, name)

    def test_test_names_follow_runner_pattern(self):
        files = sorted(EXAMPLES.glob("test_b*.py"))
        self.assertGreaterEqual(len(files), len(REQUIRED))
        self.assertTrue(all(path.name.startswith("test_b") for path in files))

    def test_models_exist_for_foundation_tests(self):
        for name in REQUIRED:
            model = name.replace("test_", "", 1)
            with self.subTest(model=model):
                self.assertTrue((EXAMPLES / model).is_file())

if __name__ == "__main__":
    unittest.main()
