import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hack_assembler import assemble, AssemblyError

class HackAssemblerTests(unittest.TestCase):
    def test_existing_computer_program_matches_binary(self):
        asm = (ROOT / "hardware/nand2tetris/programs/FillRAM.asm").read_text()
        expected = (ROOT / "hardware/nand2tetris/programs/FillRAM.hack").read_text()
        self.assertEqual(assemble(asm), expected)

    def test_predefined_registers_and_devices(self):
        self.assertEqual(assemble("@R15\n@SCREEN\n@KBD\n@SP\n"),
                         "".join(f"{n:016b}\n" for n in (15, 16384, 24576, 0)))

    def test_two_pass_forward_labels_and_variables(self):
        self.assertEqual(assemble("@END\n@foo\nM=1\n@foo\nD=M\n(END)\n@END\n0;JMP\n").splitlines(),
                         [f"{5:016b}", f"{16:016b}", "1110111111001000", f"{16:016b}",
                          "1111110000010000", f"{5:016b}", "1110101010000111"])

    def test_dest_permutations(self):
        self.assertEqual(assemble("AMD=D|M\nMDA=D|M\n"), "1111010101111000\n"*2)

    def test_commutative_alias(self):
        self.assertEqual(assemble("D=M+D\n"), assemble("D=D+M\n"))

    def test_comments_and_empty(self):
        self.assertEqual(assemble(" // nothing\n\n"), "")

    def test_reject_bad_input(self):
        for source in ("@32768", "@-1", "@", "(LOOP)\n(LOOP)", "(R0)", "D=Q", "D;BAD",
                       "AA=D", "D==M", "(invalid name)", "D=A;JMP;JMP", "=D", "D;"):
            with self.subTest(source=source):
                with self.assertRaises(AssemblyError):
                    assemble(source)

    def test_last_variable_before_screen_is_accepted(self):
        # Variables occupy 16..16383; the 16368th distinct variable lands on 16383.
        source = "".join(f"@v{i}\n" for i in range(16384 - 16))
        self.assertEqual(assemble(source).splitlines()[-1], f"{16383:016b}")

    def test_variable_collision_with_screen_is_rejected(self):
        source = "".join(f"@v{i}\n" for i in range(16384 - 16 + 1))
        with self.assertRaisesRegex(AssemblyError, "SCREEN"):
            assemble(source)

    def test_label_beyond_rom_limit(self):
        source = "@0\n" * 32768 + "(TOO_FAR)\n"
        with self.assertRaisesRegex(AssemblyError, "label address"):
            assemble(source)

    def test_line_numbers(self):
        with self.assertRaisesRegex(AssemblyError, "line 3"):
            assemble("// comment\n@1\nD=Q")
