"""Modelo de checklist de integração; NÃO executa QEMU nem verifica disco."""
REQUIRED=("boot","two_programs","isolation","write","reboot","readback")
class IncompleteEvidence(ValueError): pass
def assess(evidence):
    if not isinstance(evidence,dict): raise TypeError("evidência deve ser dicionário")
    missing=[name for name in REQUIRED if evidence.get(name) is not True]
    if missing: raise IncompleteEvidence("faltando: "+", ".join(missing))
    return True
