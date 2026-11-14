"""Parser didático; não executa comandos no sistema operacional."""
class CommandError(ValueError): pass
def parse(line):
    if not isinstance(line,str): raise CommandError("entrada não textual")
    tokens=line.split()
    if not tokens: raise CommandError("comando vazio")
    command,*args=tokens
    if command=="help" and not args: return ("help",[])
    if command=="echo": return ("echo",args)
    if command=="exit" and not args: return ("exit",[])
    raise CommandError("comando ou argumentos inválidos")
def evaluate(line):
    command,args=parse(line)
    if command=="help": return "help echo exit"
    if command=="echo": return " ".join(args)
    return "bye"
