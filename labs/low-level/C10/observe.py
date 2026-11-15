#!/usr/bin/env python3
"""Inspect live process state through Linux procfs, not simulated metrics."""
import json
import os
from pathlib import Path

def inspect(pid=None):
    pid = os.getpid() if pid is None else pid
    root = Path("/proc") / str(pid)
    status = (root / "status").read_text()
    fields = dict(line.split(":", 1) for line in status.splitlines() if ":" in line)
    stat = (root / "stat").read_text()
    # stat comm may contain spaces or parentheses: parse after final ')'.
    tail = stat.rsplit(")", 1)[1].strip().split()
    return {"pid": int(fields["Pid"].strip()),
            "ppid": int(fields["PPid"].strip()),
            "state": tail[0],
            "threads": int(fields["Threads"].strip()),
            "vmrss_kb": int(fields.get("VmRSS", "0 kB").strip().split()[0]),
            "maps_count": len((root / "maps").read_text().splitlines())}

if __name__ == "__main__":
    print(json.dumps(inspect(), sort_keys=True))
