#!/usr/bin/env python3
import platform
import subprocess
import sys
from pathlib import Path
if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C07 requires Linux x86-64")
binary = Path(__file__).with_name("flags-demo").resolve()
p = subprocess.run([str(binary)], capture_output=True, timeout=5)
assert p.returncode == 0 and not p.stderr, p
assert p.stdout == b"PASS: C07 carry, overflow and bitwise operations\n", p.stdout
asm = subprocess.run(["objdump", "-d", str(binary)], capture_output=True, text=True, check=True).stdout
assert "setb" in asm or "setc" in asm, "missing carry capture"
assert "seto" in asm, "missing overflow capture"
print("PASS: C07 arithmetic and flags")
