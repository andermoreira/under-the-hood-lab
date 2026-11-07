#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TESTS="$ROOT/hardware/nand2tetris/tests"
if [[ -z "${N2T_HOME:-}" ]]; then
  echo "NOT_RUN: set N2T_HOME to the extracted nand2tetris tools directory" >&2
  exit 2
fi
if [[ -x "$N2T_HOME/HardwareSimulator.sh" ]]; then
  SIM="$N2T_HOME/HardwareSimulator.sh"
elif [[ -x "$N2T_HOME/tools/HardwareSimulator.sh" ]]; then
  SIM="$N2T_HOME/tools/HardwareSimulator.sh"
else
  echo "NOT_RUN: HardwareSimulator.sh not found in N2T_HOME" >&2
  exit 2
fi
cd "$TESTS"
for test in Not And; do
  echo "Running $test.tst"
  "$SIM" "$test.tst"
done
echo "PASS: HDL scripts completed"
