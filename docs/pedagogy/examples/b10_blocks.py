"""Modelo em memória: não implementa filesystem nem durabilidade real."""
def split_blocks(data, block_size):
    if block_size<=0: raise ValueError("tamanho de bloco inválido")
    return [data[i:i+block_size] for i in range(0,len(data),block_size)]
def join_blocks(blocks):
    return b"".join(blocks)
def block_count(length, block_size):
    if length<0 or block_size<=0: raise ValueError("parâmetros inválidos")
    return (length+block_size-1)//block_size
