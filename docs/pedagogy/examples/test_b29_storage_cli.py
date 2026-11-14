import json
import subprocess
import sys
import unittest
from pathlib import Path
from b10_experiment_cli import experiment

SCRIPT = Path(__file__).with_name("b10_experiment_cli.py")

class BlockExperimentCLITests(unittest.TestCase):
    def test_roundtrip_passes(self):
        result = experiment(b"abcdefghij", 4)
        self.assertEqual(result["integrity"], "PASS")
        self.assertEqual(result["blocks"], 3)
        self.assertEqual(result["input_sha256"], result["recovered_sha256"])

    def test_dropped_block_fails(self):
        result = experiment(b"abcdefghij", 4, True)
        self.assertEqual(result["integrity"], "FAIL")
        self.assertNotEqual(result["input_sha256"], result["recovered_sha256"])

    def test_empty_payload_stays_valid(self):
        self.assertEqual(experiment(b"", 8)["integrity"], "PASS")

    def test_invalid_size_rejected(self):
        self.assertRaises(ValueError, experiment, b"a", 0)

    def test_cli_exit_code_detects_loss(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--text", "abc", "--drop-last"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["integrity"], "FAIL")

if __name__ == "__main__":
    unittest.main()
