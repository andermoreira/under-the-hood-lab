#!/usr/bin/env python3
import json
import unittest
from pathlib import Path
data = json.loads(Path(__file__).with_name("contracts.json").read_text())
class Contracts(unittest.TestCase):
    def test_no_unsupported_compatibility_claim(self):
        self.assertIn("not Linux binary compatibility", data["claim"])
        self.assertGreaterEqual(len(data["comparisons"]), 5)
        self.assertEqual(len({item["id"] for item in data["comparisons"]}), len(data["comparisons"]))
        for item in data["comparisons"]:
            self.assertIn(item["status"], {"PARTIAL", "MISSING", "UNVERIFIED"})
            self.assertTrue(item["gap"])
            self.assertTrue(item["kernel"].startswith("B"))
    def test_linux_elf_loader_not_marked_compatible(self):
        elf = next(x for x in data["comparisons"] if x["id"] == "elf")
        self.assertNotEqual(elf["status"], "PASS")
        self.assertIn("dynamic linker", elf["gap"])
if __name__ == "__main__":
    unittest.main()
