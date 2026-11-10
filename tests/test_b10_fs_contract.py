import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FilesystemContractTests(unittest.TestCase):
    def test_ata_driver_reads_and_writes_sectors(self):
        code = (ROOT / "kernel/x86_64/ata.c").read_text()
        self.assertIn("ata_read_sector", code)
        self.assertIn("ata_write_sector", code)
        self.assertIn("ATA_CMD_READ", code)
        self.assertIn("ATA_CMD_WRITE", code)
        self.assertIn("ATA_CMD_FLUSH", code)
        self.assertIn("0x1F0", code)

    def test_fs_validates_superblock_and_is_read_write(self):
        code = (ROOT / "kernel/x86_64/fs.c").read_text()
        self.assertIn("UTHLABFS", code)
        self.assertIn("int fs_read", code)
        self.assertIn("int fs_write", code)
        self.assertIn("ata_read_sector", code)
        self.assertIn("ata_write_sector", code)

    def test_disk_image_tool_produces_valid_superblock(self):
        # The image generator is part of the gate: build an image and check the
        # on-disk layout the kernel expects.
        with tempfile.TemporaryDirectory() as d:
            img = Path(d) / "disk.img"
            subprocess.run(
                [sys.executable, str(ROOT / "tools/make_disk.py"), str(img)],
                check=True,
            )
            data = img.read_bytes()
        self.assertEqual(data[:8], b"UTHLABFS")
        entry_count = struct.unpack_from("<I", data, 8)[0]
        self.assertEqual(entry_count, 1)
        # Directory entry 0 at LBA 1: name then start_lba/size/capacity.
        name = data[512 : 512 + 48].split(b"\x00", 1)[0]
        self.assertEqual(name, b"greeting.txt")
        start, size, cap, _ = struct.unpack_from("<IIII", data, 512 + 48)
        self.assertGreaterEqual(start, 2)
        self.assertEqual(size, len(b"disk-v1\n"))
        self.assertGreaterEqual(cap, 1)
        # The seeded content lives at the file's start sector.
        self.assertEqual(data[start * 512 : start * 512 + size], b"disk-v1\n")

    def test_boot_gate_proves_persistence(self):
        boot = (ROOT / "scripts/test-kernel-boot.sh").read_text()
        build = (ROOT / "scripts/build-kernel.sh").read_text()
        main = (ROOT / "kernel/x86_64/main.c").read_text()
        self.assertIn("B10_FS_OK", boot)
        self.assertIn("make_disk.py", boot)
        self.assertIn("if=ide", boot)
        self.assertIn("ata.o", build)
        self.assertIn("fs.o", build)
        self.assertIn("filesystem_selftest", main)
        # The test must prove a rewrite persisted, not just a read.
        self.assertIn("disk-v2!", main)


if __name__ == "__main__":
    unittest.main()
