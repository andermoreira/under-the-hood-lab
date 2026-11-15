#!/usr/bin/env python3
import platform
import signal
import subprocess
import sys
from pathlib import Path
if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C09 requires Linux x86-64")
binary = str(Path(__file__).with_name("crash").resolve())
ok = subprocess.run([binary, "ok"], capture_output=True, timeout=5)
assert ok.returncode == 0 and ok.stdout == b"C09_OK\n" and not ok.stderr
bad = subprocess.run([binary, "abort"], capture_output=True, timeout=5)
assert bad.returncode == -signal.SIGABRT, (bad.returncode, bad.stderr)
assert b"C09_BEFORE_ABORT" in bad.stderr
invalid = subprocess.run([binary, "unknown"], capture_output=True, timeout=5)
assert invalid.returncode == 2
print("PASS: C09 real normal exit, SIGABRT and invalid mode")
