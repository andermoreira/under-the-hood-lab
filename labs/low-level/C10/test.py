#!/usr/bin/env python3
import os
import platform
import sys
import unittest
from observe import inspect

class ProcObservabilityTests(unittest.TestCase):
    def test_current_process(self):
        if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
            self.skipTest("Linux x86-64 required")
        result = inspect()
        self.assertEqual(result["pid"], os.getpid())
        self.assertEqual(result["ppid"], os.getppid())
        self.assertGreaterEqual(result["threads"], 1)
        self.assertGreater(result["maps_count"], 0)

    def test_missing_process_is_not_silent(self):
        if sys.platform != "linux":
            self.skipTest("Linux required")
        with self.assertRaises(FileNotFoundError):
            inspect(999999999)

if __name__ == "__main__":
    unittest.main()
