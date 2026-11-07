import unittest

# Reference only: this tests the expected instruction sequence, NOT HDL wiring.
PROGRAM = [
    0b0000000000000010, # @2
    0b1110110000010000, # D=A
    0b0000000000000000, # @0
    0b1110001100001000, # M=D
    0b0000000000000101, # @5
    0b1110101010000111, # 0;JMP
]

class MinimalComputer:
    def __init__(self, program):
        self.rom=program
        self.ram=[0]*16384
        self.a=self.d=self.pc=0

    def step(self):
        instr=self.rom[self.pc]
        old_a=self.a
        if instr&0x8000==0:
            self.a=instr&0x7fff
            self.pc=(self.pc+1)&0x7fff
        elif instr==0b1110110000010000: # D=A
            self.d=old_a
            self.pc=(self.pc+1)&0x7fff
        elif instr==0b1110001100001000: # M=D
            self.ram[old_a]=self.d
            self.pc=(self.pc+1)&0x7fff
        elif instr==0b1110101010000111: # 0;JMP
            self.pc=old_a&0x7fff
        else:
            raise ValueError("unsupported instruction in minimal reference")

class ComputerTests(unittest.TestCase):
    def test_program_writes_ram_and_loops(self):
        machine=MinimalComputer(PROGRAM)
        for _ in range(6): machine.step()
        self.assertEqual(machine.ram[0],2)
        self.assertEqual(machine.pc,5)
        machine.step()
        self.assertEqual(machine.pc,5)

    def test_program_binary_words(self):
        self.assertEqual(len(PROGRAM),6)
        self.assertTrue(all(0<=word<=0xffff for word in PROGRAM))

    def test_negative_control_wrong_destination(self):
        machine=MinimalComputer(PROGRAM)
        for _ in range(6): machine.step()
        self.assertNotEqual(machine.ram[1],2)
