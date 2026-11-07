import unittest

MASK=0xffff

def alu(x,y,zx,nx,zy,ny,f,no):
    if zx: x=0
    if nx: x=(~x)&MASK
    if zy: y=0
    if ny: y=(~y)&MASK
    out=((x+y) if f else (x&y))&MASK
    if no: out=(~out)&MASK
    return out

class HackCPU:
    def __init__(self):
        self.a=0
        self.d=0
        self.pc=0

    def cycle(self,instruction,in_m=0,reset=0):
        old_a=self.a
        is_c=bool(instruction&0x8000)
        if is_c:
            y=in_m if instruction&0x1000 else old_a
            controls=tuple((instruction>>i)&1 for i in (11,10,9,8,7,6))
            out=alu(self.d,y,*controls)
            zero=out==0
            negative=bool(out&0x8000)
            jump=bool(((instruction&1) and not(zero or negative)) or
                      ((instruction&2) and zero) or
                      ((instruction&4) and negative))
            dest_a=bool(instruction&0x20)
            dest_d=bool(instruction&0x10)
            write_m=bool(instruction&0x08)
        else:
            out=alu(self.d,old_a,*tuple((instruction>>i)&1 for i in (11,10,9,8,7,6)))
            jump=dest_a=dest_d=write_m=False
        if reset: self.pc=0
        elif jump: self.pc=old_a&0x7fff
        else: self.pc=(self.pc+1)&0x7fff
        if not is_c: self.a=instruction&0x7fff
        elif dest_a: self.a=out
        if dest_d: self.d=out
        return out,int(write_m),old_a&0x7fff,self.pc

def c(comp,dest=0,jump=0,a=0):
    return 0xe000 | (a<<12) | (comp<<6) | (dest<<3) | jump

class CPUTests(unittest.TestCase):
    def test_a_instruction_and_pc(self):
        cpu=HackCPU()
        cpu.cycle(21)
        self.assertEqual((cpu.a,cpu.pc),(21,1))

    def test_d_equals_a_then_add(self):
        cpu=HackCPU()
        cpu.cycle(7)
        cpu.cycle(c(0b110000,dest=0b010)) # D=A
        self.assertEqual(cpu.d,7)
        cpu.cycle(5)
        cpu.cycle(c(0b000010,dest=0b010)) # D=D+A
        self.assertEqual(cpu.d,12)

    def test_jump_uses_previous_a(self):
        cpu=HackCPU()
        cpu.cycle(25)
        cpu.cycle(c(0b101010,jump=0b111)) # 0;JMP
        self.assertEqual(cpu.pc,25)

    def test_write_m_requires_c_instruction(self):
        cpu=HackCPU()
        cpu.cycle(0x0008)
        self.assertEqual(cpu.cycle(c(0b110000,dest=0b001))[1],1)
        self.assertEqual(cpu.cycle(0x0008)[1],0)

    def test_reset_priority(self):
        cpu=HackCPU()
        cpu.cycle(25)
        cpu.cycle(c(0b101010,jump=0b111),reset=1)
        self.assertEqual(cpu.pc,0)

    def test_negative_control_jump_is_not_unconditional(self):
        cpu=HackCPU()
        cpu.cycle(25)
        cpu.cycle(c(0b101010,jump=0b001)) # 0;JGT false
        self.assertEqual(cpu.pc,2)
