#!/usr/bin/env python3
"""Validate evidence manifests. Structural gate only, never executes commands."""
import argparse
import json
import re
import sys
from pathlib import Path

STATES = {"PASS", "FAIL", "NOT_RUN", "UNVERIFIED"}
SHA = re.compile(r"^[0-9a-f]{40}$")
REQUIRED = {"experiment_id", "repository", "commit", "platform", "command",
            "exit_code", "expected", "observed", "state", "reviewer", "limitations"}

def validate(record):
    errors = []
    if not isinstance(record, dict):
        return ["manifest must be a JSON object"]
    missing = REQUIRED - record.keys()
    errors.extend("missing field: " + key for key in sorted(missing))
    if missing:
        return errors
    if not isinstance(record["experiment_id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,79}", record["experiment_id"]):
        errors.append("invalid experiment_id")
    if not isinstance(record["repository"], str) or not re.fullmatch(r"[\w.-]+/[\w.-]+", record["repository"]):
        errors.append("invalid repository")
    if record["state"] not in STATES:
        errors.append("invalid state")
    if not isinstance(record["limitations"], list) or not all(isinstance(x, str) and x.strip() for x in record["limitations"]):
        errors.append("limitations must be a list of nonempty strings")
    if record["state"] == "PASS":
        for key in ("commit", "platform", "command", "expected", "observed", "reviewer"):
            if not isinstance(record[key], str) or not record[key].strip():
                errors.append("PASS requires nonempty " + key)
        if not isinstance(record["commit"], str) or not SHA.fullmatch(record["commit"]):
            errors.append("PASS requires full 40-character commit SHA")
        if record["exit_code"] != 0 or isinstance(record["exit_code"], bool):
            errors.append("PASS requires exit_code 0")
        if not isinstance(record.get("stdout_artifact"), str) or not record["stdout_artifact"].strip():
            errors.append("PASS requires stdout_artifact path")
    elif record["state"] == "NOT_RUN":
        if record["exit_code"] is not None or record["observed"] is not None:
            errors.append("NOT_RUN cannot claim exit_code or observed result")
    return errors

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default="evidence")
    args = parser.parse_args(argv)
    root = Path(args.directory)
    if not root.is_dir():
        print("FAIL: evidence directory missing", file=sys.stderr)
        return 1
    paths = sorted(root.glob("*.json"))
    if not paths:
        print("FAIL: no evidence JSON manifests", file=sys.stderr)
        return 1
    failures = 0
    for path in paths:
        try:
            errors = validate(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors = [str(exc)]
        for error in errors:
            print(f"FAIL {path}: {error}", file=sys.stderr)
        failures += bool(errors)
    print(f"validated {len(paths)} manifests, failures={failures}")
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
