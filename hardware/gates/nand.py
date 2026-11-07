"""Modelo lógico de referência; não é simulador elétrico nem HDL."""
def nand(a,b):
    if type(a) is not int or type(b) is not int or a not in (0,1) or b not in (0,1):
        raise ValueError('Esperados dois bits')
    return 1-(a & b)
def not_gate(a): return nand(a,a)
def and_gate(a,b):
    t=nand(a,b)
    return nand(t,t)
def or_gate(a,b): return nand(nand(a,a),nand(b,b))
def xor_gate(a,b):
    t=nand(a,b)
    return nand(nand(a,t),nand(b,t))
