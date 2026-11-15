#!/usr/bin/env python3
import platform
import subprocess
import sys
from pathlib import Path

if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C11 requires Linux x86-64")
root = Path(__file__).resolve().parent
for name in ("dynamic", "static"):
    binary = root / name
    result = subprocess.run([str(binary)], capture_output=True, timeout=5)
    assert result.returncode == 0 and result.stdout == b"C11_DYNAMIC_LIBC_OK\n" and not result.stderr, result
    elf = subprocess.run(["readelf", "-l", str(binary)], capture_output=True, text=True, check=True).stdout
    assert ("INTERP" in elf) == (name == "dynamic"), name
    dynamic = subprocess.run(["readelf", "-d", str(binary)], capture_output=True, text=True, check=False)
    if name == "dynamic":
        assert "NEEDED" in dynamic.stdout, dynamic.stdout
    else:
        assert "NEEDED" not in dynamic.stdout, dynamic.stdout
print("PASS: C11 static/dynamic binaries, interpreter and dependencies")
