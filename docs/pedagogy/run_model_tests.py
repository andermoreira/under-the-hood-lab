#!/usr/bin/env python3
"""Run every standalone pedagogical model test; no QEMU/kernel validation implied."""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "docs" / "pedagogy" / "examples"

def main():
    tests = sorted(EXAMPLES.glob("test_b*.py"))
    if not tests:
        print("ERROR: no pedagogical model tests found", file=sys.stderr)
        return 2
    print(f"Discovered {len(tests)} pedagogical test modules", flush=True)
    command = [sys.executable, "-m", "unittest", "discover", "-s", str(EXAMPLES), "-p", "test_b*.py", "-v"]
    return subprocess.call(command, cwd=ROOT)

if __name__ == "__main__":
    raise SystemExit(main())
