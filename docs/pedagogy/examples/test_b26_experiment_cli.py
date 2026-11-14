import json
import subprocess
import sys
import unittest
from pathlib import Path
from b05_experiment_cli import simulate

SCRIPT = Path(__file__).with_name("b05_experiment_cli.py")

class ExperimentCLITests(unittest.TestCase):
    def test_expected_trace(self):
        result = simulate([2, 4], ["alloc", "alloc", "alloc", "free:2", "alloc"])
        self.assertEqual([item["status"] for item in result],
                         ["PASS", "PASS", "EXHAUSTED", "PASS", "PASS"])
        self.assertEqual(result[-1]["frame"], 2)

    def test_double_free_visible(self):
        result = simulate([1], ["alloc", "free:1", "free:1"])
        self.assertEqual(result[-1]["status"], "INVALID_FREE")

    def test_invalid_frame_configuration_rejected(self):
        for frames in ([1, 1], [-1, 2]):
            with self.subTest(frames=frames):
                self.assertRaises(ValueError, simulate, frames, ["alloc"])

    def test_unknown_operation_rejected(self):
        self.assertRaises(ValueError, simulate, [1], ["erase"])

    def test_cli_outputs_machine_readable_trace(self):
        process = subprocess.run([sys.executable, str(SCRIPT), "--frames", "1",
                                  "--ops", "alloc,alloc"], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual([item["status"] for item in json.loads(process.stdout)],
                         ["PASS", "EXHAUSTED"])

if __name__ == "__main__":
    unittest.main()
