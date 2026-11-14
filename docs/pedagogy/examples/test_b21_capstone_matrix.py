"""Capstone checklist completeness under independent single-fault injection."""
import unittest
from b12_capstone import REQUIRED, IncompleteEvidence, assess

class CapstoneMatrix(unittest.TestCase):
    def test_complete_evidence_passes(self):
        self.assertIs(assess({key: True for key in REQUIRED}), True)

    def test_each_missing_requirement_fails_independently(self):
        for key in REQUIRED:
            evidence = {name: True for name in REQUIRED}
            del evidence[key]
            with self.subTest(key=key):
                with self.assertRaises(IncompleteEvidence) as ctx:
                    assess(evidence)
                self.assertIn(key, str(ctx.exception))

    def test_each_false_requirement_fails_independently(self):
        for key in REQUIRED:
            evidence = {name: True for name in REQUIRED}
            evidence[key] = False
            with self.subTest(key=key):
                self.assertRaises(IncompleteEvidence, assess, evidence)

    def test_truthy_values_do_not_pass(self):
        for value in (1, "PASS", [], [True]):
            evidence = {name: True for name in REQUIRED}
            evidence["boot"] = value
            with self.subTest(value=repr(value)):
                self.assertRaises(IncompleteEvidence, assess, evidence)

    def test_wrong_container_type_is_rejected(self):
        for value in (None, [], "PASS", True):
            with self.subTest(value=repr(value)):
                self.assertRaises(TypeError, assess, value)

if __name__ == "__main__":
    unittest.main()
