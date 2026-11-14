#!/usr/bin/env python3
"""ELF structure + behavior verification, Linux x86-64, GNU readelf."""
import platform
import re
import subprocess
import sys
from pathlib import Path

if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
    raise SystemExit("C02 requires Linux x86-64")
binary = Path(__file__).with_name("anatomy").resolve()

def run(*args):
    return subprocess.run(args, capture_output=True, check=True, text=True, timeout=10).stdout

p = subprocess.run([str(binary)], capture_output=True, timeout=5, check=False)
assert p.returncode == 0, f"exit={p.returncode} stderr={p.stderr!r}"
assert p.stdout == b"ELF sections and segments!\n", p.stdout
assert p.stderr == b"", p.stderr

header = run("readelf", "-h", str(binary))
assert "ELF64" in header and "Advanced Micro Devices X86-64" in header
entry = re.search(r"Entry point address:\s*(0x[0-9a-fA-F]+)", header)
assert entry and int(entry.group(1), 16) > 0, header

sections = run("readelf", "-W", "-S", str(binary))
for name in (".text", ".rodata", ".data", ".bss"):
    assert re.search(r"\]\s+" + re.escape(name) + r"\s+", sections), name
assert re.search(r"\]\s+\.bss\s+NOBITS\s+", sections), "bss should be NOBITS"

segments = run("readelf", "-W", "-l", str(binary))
assert re.search(r"^\s*LOAD\s+", segments, re.MULTILINE), "missing PT_LOAD"
symbols = run("readelf", "-W", "-s", str(binary))
assert re.search(r"\b_start\b", symbols), "missing _start"
disassembly = run("objdump", "-d", str(binary))
assert disassembly.count("syscall") >= 2, "missing syscall instructions"
print("PASS: C02 execution, ELF header, sections, PT_LOAD, symbols, disassembly")
