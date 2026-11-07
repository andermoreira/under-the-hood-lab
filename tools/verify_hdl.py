#!/usr/bin/env python3
"""Small independent NAND-only *combinational subset* verifier.

Not an implementation of the official Nand2Tetris HDL language.
Supports one-bit IN/OUT, NAND parts, acyclic connections, .cmp tables.
"""
import argparse
import itertools
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHIPS = ROOT / "hardware" / "nand2tetris"
TESTS = CHIPS / "tests"

def parse(path):
    source = re.sub(r"//[^\n]*", "", path.read_text())
    chip = re.search(r"CHIP\s+(\w+)\s*\{(.*?)\}", source, re.S)
    if not chip or chip.group(1) != path.stem:
        raise ValueError(f"Invalid CHIP declaration in {path}")
    body = chip.group(2)
    inputs = re.search(r"\bIN\s+([^;]+);", body)
    outputs = re.search(r"\bOUT\s+([^;]+);", body)
    parts = re.search(r"\bPARTS\s*:\s*(.*)", body, re.S)
    if not inputs or not outputs or not parts:
        raise ValueError("Missing IN, OUT or PARTS")
    ins = [x.strip() for x in inputs.group(1).split(",")]
    outs = [x.strip() for x in outputs.group(1).split(",")]
    if not ins or outs != ["out"] or len(set(ins)) != len(ins):
        raise ValueError("Only one-bit inputs and output named out supported")
    statements = [x.strip() for x in parts.group(1).split(";") if x.strip()]
    connections = []
    for stmt in statements:
        match = re.fullmatch(r"Nand\s*\(\s*a\s*=\s*(\w+)\s*,\s*b\s*=\s*(\w+)\s*,\s*out\s*=\s*(\w+)\s*\)", stmt)
        if not match:
            raise ValueError(f"Unsupported part: {stmt}")
        connections.append(match.groups())
    if not connections:
        raise ValueError("No NAND parts")
    return ins, connections

def evaluate(inputs, parts, bits):
    wires = dict(zip(inputs, bits))
    for a, b, out in parts:
        if a not in wires or b not in wires:
            raise ValueError(f"Undefined or forward reference: {a}, {b}")
        if out in wires:
            raise ValueError(f"Multiple drivers or input overwritten: {out}")
        wires[out] = 1 - (wires[a] & wires[b])
    if "out" not in wires:
        raise ValueError("Output not driven")
    return wires["out"]

def expected_rows(path, inputs):
    lines = [line for line in path.read_text().splitlines() if line.strip()]
    rows = [[col.strip() for col in line.strip().strip("|").split("|")] for line in lines]
    if rows[0] != inputs + ["out"]:
        raise ValueError(f"Unexpected compare header in {path}: {rows[0]}")
    return [tuple(int(x) for x in row) for row in rows[1:]]

def verify(name, chip_dir=CHIPS, cmp_dir=TESTS):
    inputs, parts = parse(chip_dir / f"{name}.hdl")
    actual = [(*bits, evaluate(inputs, parts, bits)) for bits in itertools.product((0, 1), repeat=len(inputs))]
    expected = expected_rows(cmp_dir / f"{name}.cmp", inputs)
    if len(expected) != len(actual) or sorted(expected) != sorted(actual):
        raise AssertionError(f"{name}: truth table mismatch\nactual={actual}\nexpected={expected}")
    return len(actual)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chips", nargs="*", default=["Not", "And", "Or", "Xor"])
    args = parser.parse_args()
    for chip in args.chips:
        n = verify(chip)
        print(f"PASS {chip}: {n} combinations")
    print("PASS: offline NAND-only subset verified; official HardwareSimulator NOT_RUN")

if __name__ == "__main__":
    main()
