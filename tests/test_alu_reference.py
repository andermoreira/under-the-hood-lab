import itertools
import unittest

MASK = 0xffff

def alu(x,y,zx,nx,zy,ny,f,no):
    x &= MASK
    y &= MASK
    if zx: x=0
    if nx: x=(~x)&MASK
    if zy: y=0
    if ny: y=(~y)&MASK
    out=((x+y) if f else (x&y))&MASK
    if no: out=(~out)&MASK
    return out,int(out==0),int(bool(out&0x8000))

class ALUTests(unittest.TestCase):
    def test_standard_hack_control_words(self):
        # controls (zx,nx,zy,ny,f,no), expected function
        cases=[
          ((1,0,1,0,1,0),lambda x,y:0),
          ((1,1,1,1,1,1),lambda x,y:1),
          ((1,1,1,0,1,0),lambda x,y:0xffff),
          ((0,0,1,1,0,0),lambda x,y:x),
          ((1,1,0,0,0,0),lambda x,y:y),
          ((0,0,1,1,0,1),lambda x,y:(~x)),
          ((1,1,0,0,0,1),lambda x,y:(~y)),
          ((0,0,1,1,1,1),lambda x,y:-x),
          ((1,1,0,0,1,1),lambda x,y:-y),
          ((0,1,1,1,1,1),lambda x,y:x+1),
          ((1,1,0,1,1,1),lambda x,y:y+1),
          ((0,0,1,1,1,0),lambda x,y:x-1),
          ((1,1,0,0,1,0),lambda x,y:y-1),
          ((0,0,0,0,1,0),lambda x,y:x+y),
          ((0,1,0,0,1,1),lambda x,y:x-y),
          ((0,0,0,1,1,1),lambda x,y:y-x),
          ((0,0,0,0,0,0),lambda x,y:x&y),
          ((0,1,0,1,0,1),lambda x,y:x|y),
        ]
        for x,y in [(0,0),(0xffff,1),(0x8000,0x7fff),(0x1234,0xabcd)]:
            for control,fn in cases:
                with self.subTest(x=x,y=y,control=control):
                    result,zr,ng=alu(x,y,*control)
                    self.assertEqual(result,fn(x,y)&MASK)
                    self.assertEqual(zr,int(result==0))
                    self.assertEqual(ng,(result>>15)&1)

    def test_all_controls_and_flag_invariants(self):
        for control in itertools.product((0,1),repeat=6):
            for x,y in [(0,0),(0xffff,0xffff),(0x8000,1)]:
                out,zr,ng=alu(x,y,*control)
                self.assertEqual(zr,int(out==0))
                self.assertEqual(ng,(out>>15)&1)

    def test_negative_control_add_vs_and(self):
        self.assertNotEqual(alu(1,1,0,0,0,0,1,0)[0],
                            alu(1,1,0,0,0,0,0,0)[0])
