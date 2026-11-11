import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).with_name("validate_evidence.py")
spec = importlib.util.spec_from_file_location("validate_evidence", SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

BASE = {
    "experiment_id": "demo-001", "repository": "example/lab",
    "commit": None, "platform": None, "command": "python3 demo.py",
    "exit_code": None, "expected": "prints ok", "observed": None,
    "state": "NOT_RUN", "reviewer": None, "limitations": ["local example only"]
}

class EvidenceTests(unittest.TestCase):
    def test_not_run_is_valid(self):
        self.assertEqual(mod.validate(BASE), [])

    def test_not_run_cannot_claim_success(self):
        self.assertTrue(mod.validate({**BASE, "exit_code": 0}))

    def test_fake_pass_rejected(self):
        self.assertTrue(mod.validate({**BASE, "state": "PASS", "exit_code": 0}))

    def test_valid_pass(self):
        record = {**BASE, "state": "PASS", "commit": "a" * 40,
                  "platform": "Linux x86_64", "observed": "ok", "reviewer": "reviewer",
                  "exit_code": 0, "stdout_artifact": "artifacts/output.txt"}
        self.assertEqual(mod.validate(record), [])

    def test_unknown_status(self):
        self.assertTrue(mod.validate({**BASE, "state": "APPROVED"}))

    def test_missing_field(self):
        record = dict(BASE)
        del record["limitations"]
        self.assertTrue(mod.validate(record))

    def test_directory_fails_without_manifests(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(mod.main([tmp]), 1)

    def test_directory_accepts_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "sample.json").write_text(json.dumps(BASE))
            self.assertEqual(mod.main([tmp]), 0)

if __name__ == "__main__":
    unittest.main()
