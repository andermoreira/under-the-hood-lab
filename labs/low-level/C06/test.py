#!/usr/bin/env python3
import platform
import re
import subprocess
import sys
from pathlib import Path
if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C06 requires Linux x86-64")
binary = Path(__file__).with_name("memory").resolve()
p = subprocess.run([str(binary)], capture_output=True, text=True, timeout=5)
assert p.returncode == 0 and not p.stderr, p
assert "PASS: C06 memory regions and mmap" in p.stdout, p.stdout
for name in ("stack", "data", "bss", "heap", "mmap"):
    assert re.search(r"\b" + name + r"=0x[0-9a-f]+", p.stdout), p.stdout
m = re.search(r"pagesize=(\d+)", p.stdout)
assert m and int(m.group(1)) >= 4096, p.stdout
print("PASS: C06 regions, page size, mmap write/read and cleanup")
