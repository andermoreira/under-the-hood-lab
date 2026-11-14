#!/usr/bin/env python3
"""Black-box tests for Linux x86-64 syscall copy utility."""
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C03 requires Linux x86-64")
binary = Path(__file__).with_name("copy").resolve()

def invoke(*args):
    return subprocess.run([str(binary), *map(str, args)], capture_output=True, timeout=5)

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    src, dst = root / "input", root / "output"
    for data in (b"", b"abc\x00def\n", bytes(range(256)) * 40):
        src.write_bytes(data)
        p = invoke(src, dst)
        assert (p.returncode, p.stdout, p.stderr) == (0, b"", b""), p
        assert dst.read_bytes() == data, "copy differs from source"
    p = invoke(root / "missing", dst)
    assert p.returncode == 1 and b"syscall failed" in p.stderr, p
    p = invoke(src, root / "missing-parent" / "output")
    assert p.returncode == 1 and b"syscall failed" in p.stderr, p
    for args in ((), (src,), (src, dst, "extra")):
        p = invoke(*args)
        assert p.returncode == 2 and b"usage:" in p.stderr, p
print("PASS: C03 empty/binary/multibuffer copies, missing files, bad arguments")
