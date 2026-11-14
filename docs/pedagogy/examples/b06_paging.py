"""Modelo educacional de paginação: NÃO emula MMU x86-64."""
PAGE_SIZE = 4096

class PageFault(Exception):
    pass

def translate(virtual_address: int, page_table: dict[int, tuple[int, bool]]) -> int:
    """Tabela: página virtual -> (frame físico, gravável)."""
    if virtual_address < 0:
        raise ValueError("endereço virtual negativo")
    page, offset = divmod(virtual_address, PAGE_SIZE)
    if page not in page_table:
        raise PageFault(f"página {page} não mapeada")
    frame, _writable = page_table[page]
    if frame < 0:
        raise ValueError("frame físico negativo")
    return frame * PAGE_SIZE + offset

def write_address(virtual_address: int, page_table: dict[int, tuple[int, bool]]) -> int:
    page, _offset = divmod(virtual_address, PAGE_SIZE)
    physical = translate(virtual_address, page_table)
    if not page_table[page][1]:
        raise PageFault(f"escrita proibida na página {page}")
    return physical

if __name__ == "__main__":
    table = {2: (7, False), 3: (9, True)}
    for address in (0x2005, 0x3000):
        print(f"virtual=0x{address:04x} físico=0x{translate(address, table):04x}")
