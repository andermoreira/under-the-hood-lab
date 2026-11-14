"""Dispatcher didático; NÃO realiza transição real ring 3 → ring 0."""
class SyscallError(Exception): pass
def dispatch(number, argument, memory):
    if not isinstance(number,int) or number not in (1,2): raise SyscallError("syscall desconhecida")
    if not isinstance(argument,int) or argument<0: raise SyscallError("argumento inválido")
    if number==1:
        if argument>=len(memory): raise SyscallError("ponteiro fora da memória")
        return memory[argument]
    if argument>255: raise SyscallError("código de saída inválido")
    return argument
