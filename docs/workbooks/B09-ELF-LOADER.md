# B09 — Carregador ELF: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## 1. Fenômeno
No B08 o programa de usuário era um punhado de bytes copiado cru para uma página. Programas reais vêm como arquivos ELF, com cabeçalho, seções e endereços de carga. Como o kernel pega um arquivo ELF e o transforma em um processo que roda em ring 3, colocando cada pedaço no endereço virtual certo?

## 2. Previsão (preencher antes de executar)
- Quais campos do cabeçalho ELF o loader precisa validar antes de confiar no arquivo, e o que cada um protege?
- Um segmento `PT_LOAD` tem `p_filesz = 0x40` e `p_memsz = 0x1000`. O que o loader faz com os `0xfc0` bytes que existem em memória mas não no arquivo?
- Por que o programa é linkado em `0x600000` e não em `0x400000` (dica: o que o B08 já mapeou)?
- O que acontece se `e_entry` apontar para um endereço que nenhum `PT_LOAD` cobre?

## 3. Analogia
O ELF é uma planta baixa de uma casa pré-fabricada: o cabeçalho diz "é uma planta válida, versão X"; cada `PT_LOAD` é um cômodo com a instrução "monte isto naquele lugar". O loader é a equipe que lê a planta e ergue a casa no terreno (espaço de endereços).

## 4. Onde a analogia falha
A "planta" e a "casa" compartilham os mesmos tijolos: os bytes do arquivo são copiados, não referenciados. E parte dos cômodos (`.bss`) vem sem tijolos — só a instrução "deixe este espaço vazio e zerado". A equipe também não confia na planta: valida cada medida, porque uma planta maliciosa tentaria construir dentro do espaço do kernel (por isso a checagem `p_vaddr` na metade baixa).

## 5. Faça
1. Leia `kernel/x86_64/elf.c`, o programa `userland/hello.S`/`hello.ld` e como `embed.S` embute o ELF no kernel.
2. Rode `x86_64-linux-gnu-readelf -l build/kernel/hello.elf` e confira os `PT_LOAD`.
3. Rode `make test-kernel-boot` e confirme `B09_ELF_HELLO` e `B09_ELF_OK`.

## 6. Refute
- Numa cópia, inverta a checagem de `e_machine`: o loader rejeita o ELF válido? (Controle negativo verificado: boot falha com "loaded ELF program SYS_write output not observed".)
- Faça `p_filesz > p_memsz` passar: que garantia se perde?
- Ligue `paging_map_user_page` para um segmento que invade a metade alta: o que a checagem `p_vaddr >= 0x0000800000000000` impede?

## 7. Explique sem analogia
Explique sem a planta/casa: o papel de `e_phoff`/`e_phnum`/`e_phentsize`, por que se copia `p_filesz` e se zera até `p_memsz`, e por que o loader mapeia página a página cobrindo `[p_vaddr, p_vaddr+p_memsz)` em vez de assumir alinhamento.

## 8. Transfira
Hoje o ELF é embutido no kernel (não há disco). No B10 ele virá de um sistema de arquivos. O que muda no loader quando a imagem não está mais em memória contígua mapeada, e sim em blocos de disco a serem lidos sob demanda?

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário (`docs/journal/B09.md`).

## 10. Evidência e limites
Gate ENG: `B09_ELF_HELLO` (impresso pelo programa ELF carregado, em ring 3) e `B09_ELF_OK` no boot, local e na CI. Limites: só `ET_EXEC` (sem PIE/relocações, sem linker dinâmico); todos os segmentos mapeados como graváveis (sem proteção por segmento); sem `PT_INTERP`; a imagem é embutida no kernel (disco é B10). Achado relacionado: habilitar `syscall` sem preservar o bit NXE do EFER transformava páginas read-only do kernel (com bit NX) em falhas de "bit reservado" — corrigido lendo o EFER como EDX:EAX e mantendo NXE.

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- Validar: magic `\x7fELF` (é ELF), classe 64 (ponteiros de 64 bits), endianness little (ordem dos bytes), `ET_EXEC` (executável com endereços fixos), `e_machine` x86-64 (ISA correta), `e_phentsize` (tamanho esperado do header de programa).
- `p_memsz > p_filesz`: copia `p_filesz` bytes do arquivo e deixa o resto (a cauda `.bss`) zerado, confiando no frame recém-alocado já zerado.
- Base `0x600000`: o B08 já mapeou `0x400000` (código) e `0x800000` (pilha); `paging_map_user_page` recusa páginas já presentes, então o ELF precisa de um endereço livre.
- `e_entry` fora de qualquer `PT_LOAD`: o salto para ring 3 cai numa página não mapeada → `#PF` fatal; o selftest também rejeita `entry` fora da faixa de usuário.
</details>
