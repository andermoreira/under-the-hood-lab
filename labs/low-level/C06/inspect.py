#!/usr/bin/env python3
"""C06: inspect real Linux process mappings without pretending to implement an MMU."""
import ctypes
import json
import mmap
from pathlib import Path

def inspect():
    with mmap.mmap(-1, mmap.PAGESIZE, access=mmap.ACCESS_WRITE) as region:
        region[:4] = b"UTH6"
        address = ctypes.addressof(ctypes.c_char.from_buffer(region))
        maps = Path("/proc/self/maps").read_text()
        covered = False
        for line in maps.splitlines():
            bounds = line.split()[0]
            lo, hi = (int(x, 16) for x in bounds.split("-"))
            if lo <= address < hi:
                covered = True
                break
        return {"page_size": mmap.PAGESIZE, "address": hex(address),
                "mapped_in_proc": covered, "roundtrip": region[:4] == b"UTH6"}

if __name__ == "__main__":
    print(json.dumps(inspect(), sort_keys=True))
