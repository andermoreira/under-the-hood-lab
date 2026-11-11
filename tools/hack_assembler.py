#!/usr/bin/env python3
"""Two-pass Hack assembler (Nand2Tetris), with explicit diagnostics."""
import argparse
import re
from pathlib import Path

COMP = dict(zip(
    ["0","1","-1","D","A","!D","!A","-D","-A","D+1","A+1","D-1","A-1","D+A","D-A","A-D","D&A","D|A",
     "M","!M","-M","M+1","M-1","D+M","D-M","M-D","D&M","D|M"],
    ["0101010","0111111","0111010","0001100","0110000","0001101","0110001","0001111","0110011",
     "0011111","0110111","0001110","0110010","0000010","0010011","0000111","0000000","0010101",
     "1110000","1110001","1110011","1110111","1110010","1000010","1010011","1000111","1000000","1010101"]
))
JUMP = {"": "000", "JGT":"001", "JEQ":"010", "JGE":"011", "JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111"}
SYMBOL = re.compile(r"[A-Za-z_.$:][A-Za-z0-9_.$:]*\Z")
PREDEFINED = {**{f"R{i}":i for i in range(16)}, "SP":0, "LCL":1, "ARG":2, "THIS":3, "THAT":4,
              "SCREEN":16384, "KBD":24576}
COMMUTATIVE = {"A+D":"D+A","M+D":"D+M","A&D":"D&A","M&D":"D&M","A|D":"D|A","M|D":"D|M"}

class AssemblyError(ValueError):
    pass

def assemble(source: str) -> str:
    instructions = []
    symbols = dict(PREDEFINED)
    rom = 0
    for number, raw in enumerate(source.splitlines(), 1):
        line = raw.split("//", 1)[0].strip()
        if re.search(r"\s", line):
            raise AssemblyError(f"line {number}: whitespace inside instruction")
        if not line:
            continue
        if line.startswith("("):
            label = line[1:-1] if line.endswith(")") else ""
            if not SYMBOL.fullmatch(label):
                raise AssemblyError(f"line {number}: invalid label {line}")
            if label in symbols:
                raise AssemblyError(f"line {number}: duplicate or reserved label {label}")
            if rom > 32767:
                raise AssemblyError(f"line {number}: label address outside 0..32767")
            symbols[label] = rom
        else:
            instructions.append((number, line))
            rom += 1
            if rom > 32768:
                raise AssemblyError(f"line {number}: ROM exceeds 32K instructions")
    next_variable = 16
    binary = []
    for number, line in instructions:
        if line.startswith("@"):
            value = line[1:]
            if value.isascii() and value.isdecimal():
                address = int(value)
                if address > 32767:
                    raise AssemblyError(f"line {number}: A-instruction outside 0..32767")
            elif SYMBOL.fullmatch(value):
                if value not in symbols:
                    if next_variable >= 16384:
                        raise AssemblyError(
                            f"line {number}: variable space exhausted "
                            f"(would collide with SCREEN at 16384)")
                    symbols[value] = next_variable
                    next_variable += 1
                address = symbols[value]
            else:
                raise AssemblyError(f"line {number}: invalid A-instruction {line}")
            binary.append(f"{address:016b}")
            continue
        if line.count("=") > 1 or line.count(";") > 1:
            raise AssemblyError(f"line {number}: malformed C-instruction {line}")
        dest, sep, rest = line.partition("=")
        if sep and not dest:
            raise AssemblyError(f"line {number}: empty dest before '=' in {line}")
        if not sep:
            dest, rest = "", dest
        comp, semi, jump = rest.partition(";")
        if semi and not jump:
            raise AssemblyError(f"line {number}: empty jump after ';' in {line}")
        if not semi:
            jump = ""
        comp = COMMUTATIVE.get(comp, comp)
        if not comp or comp not in COMP:
            raise AssemblyError(f"line {number}: invalid comp {comp!r}")
        if jump not in JUMP:
            raise AssemblyError(f"line {number}: invalid jump {jump!r}")
        if len(dest) != len(set(dest)) or any(ch not in "ADM" for ch in dest):
            raise AssemblyError(f"line {number}: invalid dest {dest!r}")
        dest_bits = "".join("1" if ch in dest else "0" for ch in "ADM")
        binary.append("111" + COMP[comp] + dest_bits + JUMP[jump])
    return "\n".join(binary) + ("\n" if binary else "")

def main():
    parser = argparse.ArgumentParser(description="Assemble Hack .asm into 16-bit .hack")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    try:
        result = assemble(args.input.read_text(encoding="utf-8"))
    except (AssemblyError, OSError) as exc:
        parser.error(str(exc))
    target = args.output or args.input.with_suffix(".hack")
    target.write_text(result, encoding="ascii")

if __name__ == "__main__":
    main()
