#!/usr/bin/env python3
"""Functional smoke test for Linux x86-64 C01; no external packages."""
import platform
import subprocess
import sys
from pathlib import Path

if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C01 requires Linux x86-64 (use a VM on other platforms)")

binary = Path(__file__).with_name("hello")
result = subprocess.run([str(binary.resolve())], capture_output=True, timeout=5, check=False)
assert result.returncode == 0, f"unexpected exit: {result.returncode}; stderr={result.stderr!r}"
assert result.stdout == b"Hello from x86-64 assembly!\n", repr(result.stdout)
assert result.stderr == b"", repr(result.stderr)

header = subprocess.run(["readelf", "-h", str(binary)], capture_output=True, text=True, check=True).stdout
assert "ELF64" in header and "Advanced Micro Devices X86-64" in header, header
disassembly = subprocess.run(["objdump", "-d", str(binary)], capture_output=True, text=True, check=True).stdout
assert disassembly.count("syscall") >= 2, disassembly
print("PASS: C01 stdout, exit, ELF architecture, syscall instructions")
