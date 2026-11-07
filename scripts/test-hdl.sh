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
  sed -i 's@load \\../@load @g; s@ROM32K load \\../programs/@ROM32K load programs/@g' "$file"
done
cd "$STAGE"
for test in Not And Or Xor Mux HalfAdder FullAdder Add16 Inc16 ALU Bit Register RAM8 RAM64 PC CPU Computer; do
  echo "Running $test.tst"
  rm -f "$test.out"
  "$SIM" "$test.tst"
  if [[ ! -s "$test.out" ]]; then
    echo "FAIL: $test.out missing or empty" >&2
    exit 1
  fi
  python3 "$ROOT/tools/check_cmp.py" "$test.cmp" "$test.out"
  cp "$test.out" "$TESTS/$test.out"
done
echo "PASS: official simulator produced matching output for all listed circuits"
