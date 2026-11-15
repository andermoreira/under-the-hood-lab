#!/usr/bin/env python3
import platform
import re
import subprocess
import sys
from pathlib import Path
if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C08 requires Linux x86-64")
exe = str(Path(__file__).with_name("benchmark").resolve())
for iterations, chunk in [(5, 1), (3, 4096)]:
    p = subprocess.run([exe, str(iterations), str(chunk)], capture_output=True, timeout=5)
    assert p.returncode == 0, p.stderr
    assert p.stdout == bytes(iterations * chunk)
    assert re.search(rb"C08_OK iterations=%d chunk=%d bytes=%d elapsed_ns=\d+" %
                     (iterations, chunk, iterations * chunk), p.stderr), p.stderr
for args in [("0", "1"), ("1", "0"), ("-1", "4"), ("bad", "4")]:
    p = subprocess.run([exe, *args], capture_output=True, timeout=5)
    assert p.returncode != 0, (args, p)
print("PASS: C08 real writes, byte counts, invalid-input controls")
