#!/usr/bin/env python3
"""Compare Nand2Tetris output tables without trusting process exit code alone."""
import sys
from pathlib import Path

def rows(path):
    lines = [line.strip() for line in Path(path).read_text().splitlines() if line.strip()]
    if not lines or any(not (line.startswith("|") and line.endswith("|")) for line in lines):
        raise ValueError(f"Invalid or empty table: {path}")
    return [tuple(cell.strip() for cell in line[1:-1].split("|")) for line in lines]

def check(expected, observed):
    a, b = rows(expected), rows(observed)
    if a != b:
        raise AssertionError(f"Output mismatch: expected {a}, observed {b}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: check_cmp.py EXPECTED.cmp ACTUAL.out")
    check(sys.argv[1], sys.argv[2])
    print("PASS: compare output matches")
