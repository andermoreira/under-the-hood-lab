#!/usr/bin/env python3
"""Functional smoke test for C↔Assembly System V AMD64 ABI."""
import platform
import subprocess
import sys
from pathlib import Path

if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C05 requires Linux x86-64")
binary = Path(__file__).with_name("abi-demo").resolve()
p = subprocess.run([str(binary)], capture_output=True, timeout=5)
assert p.returncode == 0 and p.stderr == b"", (p.returncode, p.stderr)
assert p.stdout.count(b"PASS:") == 5, p.stdout
symbols = subprocess.run(["nm", str(binary)], capture_output=True, text=True, check=True).stdout
for symbol in ("sum_seven", "call_callback"):
    assert symbol in symbols, symbol
print("PASS: C05 executable and symbol checks")
