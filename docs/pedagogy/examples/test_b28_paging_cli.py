import json
import subprocess
import sys
import unittest
from pathlib import Path
from b06_experiment_cli import experiment
from b06_paging import PAGE_SIZE

SCRIPT = Path(__file__).with_name("b06_experiment_cli.py")

class PagingExperimentCLITests(unittest.TestCase):
    def test_permission_and_unmapped_faults(self):
        result = experiment([(2, 7, False), (3, 9, True)],
                            [("read", 2*PAGE_SIZE+5), ("write", 2*PAGE_SIZE+5),
                             ("write", 3*PAGE_SIZE), ("read", 0)])
        self.assertEqual([x["status"] for x in result], ["PASS", "FAULT", "PASS", "FAULT"])
        self.assertEqual(result[0]["physical"], 7*PAGE_SIZE+5)

    def test_negative_virtual_address_faults(self):
        self.assertEqual(experiment([(0, 0, True)], [("read", -1)])[0]["status"], "FAULT")

    def test_duplicate_page_rejected(self):
        self.assertRaises(ValueError, experiment, [(1, 2, True), (1, 3, True)], [])

    def test_unknown_operation_rejected(self):
        self.assertRaises(ValueError, experiment, [(0, 0, True)], [("execute", 0)])

    def test_cli_json_output(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["trace"]), 4)

if __name__ == "__main__":
    unittest.main()
