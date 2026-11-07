"""Static wiring contracts. These do not replace HardwareSimulator execution."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1] / "hardware/nand2tetris"

def hdl(name):
    return (ROOT / f"{name}.hdl").read_text()

class IntegrationContractTests(unittest.TestCase):
    def test_computer_has_rom_cpu_memory_and_closed_feedback(self):
        source = hdl("Computer")
        self.assertIn("ROM32K(address=pc, out=instruction)", source)
        self.assertIn("CPU(inM=memoryValue, instruction=instruction", source)
        self.assertIn("Memory(in=memoryWriteValue, load=memoryWriteEnable", source)
        self.assertIn("address=memoryAddress, out=memoryValue", source)
        self.assertIn("addressM=memoryAddress, pc=pc", source)

    def test_memory_map_selects_keyboard_only_in_upper_region(self):
        source = hdl("Memory")
        self.assertIn("Not(in=address[14], out=not14)", source)
        self.assertIn("And(a=address[14], b=address[13], out=keyboardSelect)", source)
        self.assertIn("Mux16(a=lowerOut, b=keyboardOut, sel=keyboardSelect, out=out)", source)
        self.assertIn("And(a=upperLoad, b=not13, out=screenLoad)", source)

    def test_all_local_hdl_dependencies_exist_or_are_platform_chips(self):
        native = {"Nand", "DFF", "RAM16K", "Screen", "Keyboard", "ROM32K"}
        for name in ("Computer", "Memory", "CPU", "PC", "Register", "ALU"):
            with self.subTest(chip=name):
                for part in re.findall(r"^\s*([A-Z][A-Za-z0-9]*)\(", hdl(name), re.M):
                    self.assertTrue(part in native or (ROOT / f"{part}.hdl").exists(),
                                    f"{name} depends on missing chip {part}")

    def test_official_runner_includes_integrated_computer(self):
        runner = (ROOT.parents[1] / "scripts/test-hdl.sh").read_text()
        self.assertRegex(runner, r"for test in .*\bComputer\b; do")

    def test_official_test_loads_rom_and_checks_memory(self):
        test = (ROOT / "tests/Computer.tst").read_text()
        self.assertIn("ROM32K load ../programs/FillRAM.hack", test)
        self.assertIn("RAM[0]", test)
        self.assertIn("RAM[1]", test)
        self.assertIn("repeat 6", test)
