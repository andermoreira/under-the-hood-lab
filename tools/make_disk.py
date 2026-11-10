#!/usr/bin/env python3
"""Create a disk image for the B10 toy filesystem (UTHLABFS).

Layout (512-byte sectors, little-endian):
  LBA 0     superblock: magic "UTHLABFS" + u32 entry_count
  LBA 1..   directory: fixed 64-byte entries
  data      each file occupies `capacity` contiguous sectors at start_lba

Usage: make_disk.py <out.img> [name=content ...]
Default seeds one file: greeting.txt = "disk-v1\\n".
"""
import struct
import sys

SECTOR = 512
ENTRY_SIZE = 64
NAME_MAX = 48
DIR_LBA = 1
MAGIC = b"UTHLABFS"


def build(files):
    # Directory entries first (one sector is plenty for a few files).
    per_sector = SECTOR // ENTRY_SIZE
    dir_sectors = max(1, (len(files) + per_sector - 1) // per_sector)
    data_lba = DIR_LBA + dir_sectors

    entries = []
    data = bytearray()
    lba = data_lba
    for name, content in files:
        cap = max(1, (len(content) + SECTOR - 1) // SECTOR)
        entries.append((name, lba, len(content), cap))
        block = bytearray(cap * SECTOR)
        block[: len(content)] = content
        data += block
        lba += cap

    # Superblock.
    sb = bytearray(SECTOR)
    sb[:8] = MAGIC
    struct.pack_into("<I", sb, 8, len(files))

    # Directory sectors.
    dir_blob = bytearray(dir_sectors * SECTOR)
    for i, (name, start, size, cap) in enumerate(entries):
        off = i * ENTRY_SIZE
        nb = name.encode("ascii")
        if len(nb) >= NAME_MAX:
            raise SystemExit(f"name too long: {name}")
        dir_blob[off : off + len(nb)] = nb
        struct.pack_into("<IIII", dir_blob, off + NAME_MAX, start, size, cap, 0)

    return bytes(sb) + bytes(dir_blob) + bytes(data)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: make_disk.py <out.img> [name=content ...]")
    out = sys.argv[1]
    pairs = sys.argv[2:]
    if pairs:
        files = []
        for p in pairs:
            name, _, content = p.partition("=")
            files.append((name, content.encode("ascii")))
    else:
        files = [("greeting.txt", b"disk-v1\n")]
    img = build(files)
    # Pad to a round size so QEMU is happy with an IDE geometry.
    total = ((len(img) + SECTOR - 1) // SECTOR) * SECTOR
    pad = 64 * 1024
    total = max(total, pad)
    with open(out, "wb") as f:
        f.write(img)
        f.write(b"\x00" * (total - len(img)))


if __name__ == "__main__":
    main()
