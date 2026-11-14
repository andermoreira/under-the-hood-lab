#!/usr/bin/env python3
"""Functional tests for intentionally minimal Assembly coreutils."""
import platform
import subprocess
import sys
from pathlib import Path
if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C04 requires Linux x86-64")
root = Path(__file__).parent
def run(cmd, data=b""):
    return subprocess.run([str(root / cmd[0]), *cmd[1:]], input=data, capture_output=True, timeout=5)
for args, expected in [((), b"\n"), (("hello",), b"hello\n"), (("a", "b"), b"a b\n"), (("", "x"), b" x\n")]:
    p = run(("echo", *args))
    assert p.returncode == 0 and p.stdout == expected and not p.stderr, (args, p)
for data in (b"", b"abc\x00def\n", bytes(range(256)) * 40):
    p = run(("cat",), data)
    assert p.returncode == 0 and p.stdout == data and not p.stderr, p
    p = run(("wc",), data)
    assert p.returncode == 0 and p.stdout == f"{data.count(bytes([10]))} {len(data)}\n".encode(), p
for name in ("cat", "wc"):
    assert run((name, "unexpected")).returncode != 0
print("PASS: C04 echo, streaming cat, newline/byte wc, binary and negative cases")
