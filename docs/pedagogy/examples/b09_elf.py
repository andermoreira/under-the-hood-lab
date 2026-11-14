"""Valida somente identificador ELF64 little-endian; NÃO carrega executáveis."""
class InvalidELF(ValueError): pass
def inspect_header(data):
    if len(data)<16: raise InvalidELF("identificador incompleto")
    if data[:4]!=b"\\x7fELF": raise InvalidELF("magic inválido")
    if data[4]!=2: raise InvalidELF("não é ELF64")
    if data[5]!=1: raise InvalidELF("não é little-endian")
    if data[6]!=1: raise InvalidELF("versão ELF inválida")
    return {"class":"ELF64","endian":"little"}
