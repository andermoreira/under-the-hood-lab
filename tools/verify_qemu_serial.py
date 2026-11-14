#!/usr/bin/env python3
"""Validate real QEMU serial output against mandatory kernel milestones.

This parser does NOT run QEMU; use scripts/test-kernel-boot.sh first.
"""
import argparse
import json
from pathlib import Path

REQUIRED = (
    "KERNEL_READY",
    "B05_PMM_ALLOC_FREE_OK",
    "B06_PAGING_MAP_UNMAP_OK",
    "B07_SCHEDULER_OK",
    "B08_USERMODE_OK",
    "B09_ELF_OK",
    "B10_FS_OK",
    "B11_SHELL_OK",
    "B12_CRASH_CONTAINED",
)
FORBIDDEN = ("PANIC", "KERNEL_FAULT", "EXCEPTION_UD_VECTOR_6")

def assess_serial(content):
    lines = content.splitlines()
    observed = set(lines)
    missing = [marker for marker in REQUIRED if marker not in observed]
    forbidden = [marker for marker in FORBIDDEN if any(marker in line for line in lines)]
    order_ok = "KERNEL_READY" in observed and all(
        lines.index("KERNEL_READY") < lines.index(marker)
        for marker in REQUIRED[1:] if marker in observed
    )
    return {"status": "PASS" if not missing and not forbidden and order_ok else "FAIL",
            "missing": missing, "forbidden": forbidden, "boot_before_milestones": order_ok,
            "markers_checked": list(REQUIRED)}

def main(argv=None):
    parser = argparse.ArgumentParser(description="Assess existing QEMU serial log; does not boot QEMU")
    parser.add_argument("serial_log", type=Path)
    parser.add_argument("--output", type=Path, help="optional JSON report")
    args = parser.parse_args(argv)
    if not args.serial_log.is_file():
        parser.error(f"serial log not found: {args.serial_log}")
    report = assess_serial(args.serial_log.read_text(encoding="utf-8", errors="replace"))
    encoded = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
