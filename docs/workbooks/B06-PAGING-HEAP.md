# B06 — Paginação, #PF e heap: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## Guia de fundamentos — leitura antes do PACTO

**Pré-requisitos:** [Trilha 0](../FOUNDATIONS.md), especialmente F04–F08; não exige eletrônica prévia. **Objetivo:** explicar o mecanismo antes de pedir previsões avançadas.

### Analogia do cotidiano
Um índice de biblioteca indica em qual estante está um livro. Uma tabela de páginas associa páginas virtuais a frames físicos e permissões.

**Onde a analogia falha:** A CPU usa caches de tradução (TLB); um índice alterado pode exigir invalidação. Uma entrada presente não garante que todo acesso seja permitido.

### Mecanismo, passo a passo
Uma leitura de endereço não mapeado causa #PF. CR2 registra o endereço associado à falha; o código de erro descreve aspectos do acesso.

### Exemplo resolvido
Em x86-64 de quatro níveis, o endereço virtual seleciona entradas PML4, PDPT, PD e PT; a entrada final aponta para frame físico, acrescido do deslocamento na página.

### Caso-limite e erro comum
Um heap do kernel oferece alocações de tamanho variável sobre páginas mapeadas. Alocar um frame e mapear uma página são operações distintas.

### Diagrama de fluxo
```mermaid
flowchart LR
 V[Endereço virtual] --> P[PML4]
 P --> D[PDPT]
 D --> PD[PD]
 PD --> PT[PT]
 PT --> F[Frame físico]
```

O diagrama mostra relações conceituais; não comprova temporização, privilégios ou execução real.

### Exercícios graduados
1. **Recuperação:** Diferencie frame, página virtual, PML4, CR3, TLB, #PF, heap. Por que atualizar tabela de páginas pode exigir `invlpg`?
2. **Aplicação:** desenhe o fluxo do diagrama e anote o papel de cada etapa sem usar a analogia.
3. **Transferência:** Como evitar que um mapeamento de usuário exponha uma página de supervisor? Descreva o teste negativo.

### Orientação de correção
Uma resposta adequada deve nomear as estruturas técnicas, justificar cada transição e apresentar um contraexemplo. Compare sua solução com os exemplos e o código citado no laboratório; registre dúvidas em vez de declarar compreensão sem evidência.

**Estado desta ampliação:** conteúdo editorial implementado; execução dos exemplos, teste com estudante iniciante e revisão independente **NOT_RUN**. As evidências históricas citadas no workbook original pertencem aos commits e ambientes ali identificados, não a esta alteração.

## 1. Fenômeno
O kernel usa endereços como `0xffffffff80001234`, mas a máquina tem só 128 MiB. Quem traduz esse endereço virtual para um físico e o que acontece quando não existe tradução?

## 2. Previsão (preencher antes de executar)
- Se a nova PML4 copiasse só as entradas 0–255 e zerasse 256–511, o que aconteceria logo após `mov %0, %%cr3`?
- Por que copiar só a PML4 não basta para dizer que o kernel é dono de todas as tabelas?
- Lendo `0x1000` com a metade baixa vazia, quais valores de CR2 e do código de erro você espera?
- `kmalloc(24)` devolve um ponteiro alinhado a quanto? E `kfree` duas vezes no mesmo ponteiro?

## 3. Analogia
A tabela de páginas é um índice de quatro níveis num arquivo de gavetas: andar (PML4), corredor (PDPT), armário (PD), gaveta (PT).

## 4. Onde a analogia falha
A CPU memoriza traduções recentes (TLB): mudar o índice não apaga o que ela já decorou até recarregar o CR3 ou rodar `invlpg`. E, no nosso caso, a nova PML4 aponta para corredores que ainda pertencem ao Limine.

## 5. Faça
1. Leia `kernel/x86_64/paging.c`, `heap.c`, `kmalloc.c` e `isr_page_fault` em `interrupts.S`.
2. Rode `make test-kernel-boot` e confira, em ordem: `B06_HEAP_PAGE_OK`, `B06_KMALLOC_OK`, `B06_OWN_PML4_OK`, `B06_PAGING_ROLLBACK_OK`, `B06_PAGING_MAP_UNMAP_OK`.
3. Rode a variante `KERNEL_CFLAGS=-DB06_TRIGGER_PF` com `B06_EXPECT_PF=1` e leia as linhas `EXCEPTION_PF_*`.

## 6. Refute
- Limpe o bit Present das entradas 256–511 numa cópia: o QEMU deve dar `Triple fault` e o gate deve falhar.
- Faça `kfree` não limpar o bitmap: os ciclos de reuso devem consumir frames novos e `B06_KMALLOC_FAIL` deve aparecer.
- Compile a variante #PF sem o `set_gate(14, ...)`: o que muda no `qemu-debug.log`?

## 7. Explique sem analogia
Explique como os bits 47–12 de um endereço virtual indexam os quatro níveis, o que significam os bits P, W e PS de uma entrada, e por que `paging_map_test_page` desfaz entradas recém-criadas quando uma alocação falha.

## 8. Transfira
No B08, cada processo terá sua própria metade baixa. Usando `paging_adopt_kernel_space` como ponto de partida, como você criaria um espaço de endereçamento novo por processo e o que precisaria ser copiado?

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário.

## 10. Evidência e limites
Ambiente local: Docker `ubuntu:24.04` e `ubuntu:26.04` (amd64), QEMU 8.2.2, GCC 13.3.0 e 15.2.0, Limine `v9.x-binary` @ `ee5d29c`; boot normal, teclado, #UD e #PF imprimem `PASS`, e a CI repete no `main`.

- **Heap de páginas:** páginas de 4 KiB do PMM via HHDM, zeradas, com checagem de dono e de double free.
- **kmalloc:** classes 32–1024 bytes, uma página por slab com cabeçalho e bitmap. Nunca devolve slabs vazios, não zera memória reutilizada, não tem trava (um núcleo, fora de IRQs) e confia em qualquer página que tenha a marca de slab.
- **Paginação:** map/unmap de uma página em `0xffffc00000000000`, com rollback em 4 pontos de falha injetada e devolução só das tabelas que o módulo criou.
- **PML4 própria:** metade baixa vazia, metade alta copiada do Limine. PDPT/PD/PT da metade alta continuam sendo do Limine, em memória "bootloader reclaimable" que não pode ir para o PMM.
- **#PF:** só diagnóstico (CR2 e código de erro, depois para). Sem paginação sob demanda, sem SMP nem TLB shootdown.

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- Zerar 256–511: a próxima busca de instrução (código do kernel na metade alta) não tem tradução → #PF; a IDT e a pilha também ficaram sem tradução → double fault → triple fault.
- Só a PML4 é nova; os níveis abaixo dela continuam sendo as tabelas do Limine, compartilhadas.
- CR2 = `0x1000`; código de erro `0`: página ausente (P=0), leitura (W=0), modo supervisor (U=0).
- `kmalloc(24)` usa a classe 32: ponteiro alinhado a 32. O segundo `kfree` devolve 0 (bit já limpo).
- Transferência: alocar uma PML4 por processo, copiar 256–511 (kernel compartilhado), deixar 0–255 vazias e mapear o programa com o bit U.
</details>
