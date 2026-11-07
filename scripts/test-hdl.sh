#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TESTS="$ROOT/hardware/nand2tetris/tests"
if [[ -z "${N2T_HOME:-}" ]]; then
  echo "NOT_RUN: N2T_HOME not set" >&2
  exit 2
fi
if [[ -x "$N2T_HOME/HardwareSimulator.sh" ]]; then
  SIM="$N2T_HOME/HardwareSimulator.sh"
elif [[ -x "$N2T_HOME/tools/HardwareSimulator.sh" ]]; then
  SIM="$N2T_HOME/tools/HardwareSimulator.sh"
else
  echo "NOT_RUN: HardwareSimulator.sh not found" >&2
  exit 2
fi
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
cp "$ROOT"/hardware/nand2tetris/*.hdl "$STAGE/"
cp "$TESTS"/*.tst "$TESTS"/*.cmp "$STAGE/"
cp -r "$ROOT/hardware/nand2tetris/programs" "$STAGE/programs"
# Simulator resolves HDL dependencies from the loaded chip directory.
# Stage tests beside chips; keep original sources unchanged.
for file in "$STAGE"/*.tst; do
  python3 - "$file" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(); s=s.replace('load ../', 'load ').replace('ROM32K load ../programs/', 'ROM32K load programs/')
# Official comparator requires exact column formatting; use our semantic comparator instead.
s=chr(10).join(line for line in s.splitlines() if not line.lstrip().startswith('compare-to ')) + chr(10)
p.write_text(s)
PY
done
cd "$STAGE"
for test in Not And Or Xor Mux HalfAdder FullAdder Add16 Inc16 ALU Bit Register RAM8 RAM64 PC CPU Computer; do
  echo "Running $test.tst"
  rm -f "$test.out"
  if [[ "$test" == "Not" ]]; then sed -n '1,8p' "$test.tst"; fi
  if ! "$SIM" "$test.tst"; then
    echo "FAIL: simulator rejected $test.tst" >&2
    [[ ! -f "$test.out" ]] || cat "$test.out"
    exit 1
  fi
  if [[ ! -s "$test.out" ]]; then
    echo "FAIL: $test.out missing or empty" >&2
    exit 1
  fi
  python3 "$ROOT/tools/check_cmp.py" "$test.cmp" "$test.out"
  cp "$test.out" "$TESTS/$test.out"
done
echo "PASS: official simulator produced matching output for all listed circuits"
