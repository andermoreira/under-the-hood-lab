import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "hardware/nand2tetris/programs/FillRAM.hack"
COMPUTER_TEST = ROOT / "hardware/nand2tetris/tests/Computer.tst"

class ProgramContractTests(unittest.TestCase):
    def test_program_is_six_binary_instructions(self):
        lines = PROGRAM.read_text().splitlines()
        self.assertEqual(len(lines), 6)
        self.assertTrue(all(len(line) == 16 and set(line) <= {"0", "1"} for line in lines))

    def test_program_instructions_match_contract(self):
        words = [int(line, 2) for line in PROGRAM.read_text().splitlines()]
        self.assertEqual(words, [2, 0xEC10, 0, 0xE308, 5, 0xEA87])

    def test_official_script_loads_same_program(self):
        script = COMPUTER_TEST.read_text()
        self.assertIn("ROM32K load ../programs/FillRAM.hack", script)
        self.assertIn("repeat 6", script)
        self.assertIn("RAM[0]", script)
