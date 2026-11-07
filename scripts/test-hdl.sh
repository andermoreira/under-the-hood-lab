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
cd "$TESTS"
for test in Not And Or Xor Mux HalfAdder FullAdder Add16 ALU Bit Register PC; do
  echo "Running $test.tst"
  rm -f "$test.out"
  "$SIM" "$test.tst"
  if [[ ! -s "$test.out" ]]; then
    echo "FAIL: $test.out missing or empty" >&2
    exit 1
  fi
  python3 "$ROOT/tools/check_cmp.py" "$test.cmp" "$test.out"
done
echo "PASS: official simulator produced matching output for all listed circuits"
