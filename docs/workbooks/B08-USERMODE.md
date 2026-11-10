# B08 — Ring 3 e chamadas de sistema: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## Guia de fundamentos — leitura antes do PACTO

**Pré-requisitos:** [Trilha 0](../FOUNDATIONS.md), especialmente F04–F08; não exige eletrônica prévia. **Objetivo:** explicar o mecanismo antes de pedir previsões avançadas.

### Analogia do cotidiano
Num restaurante, clientes pedem serviços à cozinha em vez de operar equipamentos restritos. Uma syscall solicita ao kernel um serviço privilegiado.

**Onde a analogia falha:** A transição é executada pela CPU; não existe um garçom independente. `syscall` não troca automaticamente para uma pilha segura em x86-64: o código de entrada precisa cuidar disso.

### Mecanismo, passo a passo
A instrução `syscall` transfere controle ao handler configurado em MSRs. Em x86-64, RCX e R11 guardam valores necessários ao retorno; a entrada precisa tratar pilha e registradores cuidadosamente.

### Exemplo resolvido
Ring 0 é privilégio de kernel; ring 3 é usuário. Páginas marcadas como supervisor não podem ser acessadas em ring 3. As permissões são verificadas pelo hardware.

### Caso-limite e erro comum
Um ponteiro de usuário pode ser inválido, não mapeado ou apontar para região protegida. O kernel deve validar acesso e comprimento antes de ler bytes.

### Diagrama de fluxo
```mermaid
flowchart LR
 U[Ring 3] --> SC[syscall]
 SC --> V[Kernel valida]
 V --> D[Serviço]
 D --> RET[Retorno a ring 3]
```

O diagrama mostra relações conceituais; não comprova temporização, privilégios ou execução real.

### Exercícios graduados
1. **Recuperação:** Explique ring 0, ring 3, bit U/S, MSR, syscall e validação de ponteiros. Por que uma syscall não significa confiança no chamador?
2. **Aplicação:** desenhe o fluxo do diagrama e anote o papel de cada etapa sem usar a analogia.
3. **Transferência:** Desenhe um pedido de escrita válido e um inválido, indicando o ponto da rejeição.

### Orientação de correção
Uma resposta adequada deve nomear as estruturas técnicas, justificar cada transição e apresentar um contraexemplo. Compare sua solução com os exemplos e o código citado no laboratório; registre dúvidas em vez de declarar compreensão sem evidência.

**Estado desta ampliação:** conteúdo editorial implementado; execução dos exemplos, teste com estudante iniciante e revisão independente **NOT_RUN**. As evidências históricas citadas no workbook original pertencem aos commits e ambientes ali identificados, não a esta alteração.

## 1. Fenômeno
Um programa de usuário não pode acessar diretamente a porta serial nem as estruturas do kernel, mas ainda assim consegue imprimir na tela. Como o processador separa "código privilegiado" (kernel, ring 0) de "código comum" (usuário, ring 3), e como um programa comum pede um favor ao kernel sem poder tocar no hardware?

## 2. Previsão (preencher antes de executar)
- Por que uma página de código do kernel (bit U/S = 0) não pode ser executada em ring 3, e o que o processador faz se tentar?
- A instrução `sysret` carrega os seletores de CS e SS a partir de um campo do MSR `STAR`. Se o kernel usa CS=0x28/SS=0x30, quais seletores de usuário o layout do `sysret` exige, e por que a ordem (+8 dados, +16 código) importa?
- Quando o usuário executa `syscall`, em qual pilha o kernel passa a rodar, e de onde vem esse endereço?
- Por que o teste "pré-toca" (zera) a pilha de kernel do syscall antes de entrar em ring 3?

## 3. Analogia
Ring 0 e ring 3 são como a cozinha e o salão de um restaurante. O cliente (ring 3) não entra na cozinha; ele faz um pedido pelo garçom (`syscall`), que leva à cozinha (ring 0), que prepara e devolve o prato (`sysret`).

## 4. Onde a analogia falha
O "garçom" não é uma pessoa separada: é a mesma CPU que muda de privilégio instantaneamente, trocando pilha e seletores em uma única instrução. E o cliente não "espera sentado" — sua execução é literalmente congelada (RIP e RFLAGS salvos em `rcx`/`r11`) até o `sysret`. A analogia também sugere confiança mútua; na prática o kernel precisa desconfiar de todo ponteiro vindo do salão (daí o limite de tamanho no `SYS_write`).

## 5. Faça
1. Leia `kernel/x86_64/usermode.c`, `usermode.S`, `userprog.S`, a GDT/TSS em `interrupts.c` e `paging_map_user_page` em `paging.c`.
2. Desenhe a transição: `usermode_enter` (sysret) → payload em ring 3 → `syscall` → `syscall_entry` → `syscall_dispatch` → `sysret` de volta.
3. Rode `make test-kernel-boot` e confirme `B08_USERLAND_HELLO` e `B08_USERMODE_OK`.

## 6. Refute
- Numa cópia, corrompa o RIP de entrada (`usermode_run(B08_USER_CODE + 0x1000, ...)`): preveja e rode. (Controle negativo verificado: o boot falha com "ring-3 SYS_write output not observed".)
- Remova o bit `USER` de `paging_map_user_page`: o que o processador faz ao buscar a primeira instrução em ring 3?
- Tire o "pré-toque" da pilha de syscall: o fault volta? Em que instrução, e por que ele é fatal naquele contexto?

## 7. Explique sem analogia
Explique sem cozinha/salão: o papel do DPL nos descritores de segmento, por que `syscall` carrega CS/SS do `STAR[47:32]` e `sysret` do `STAR[63:48]`, por que `rcx`/`r11` guardam RIP/RFLAGS, e o papel do `rsp0` da TSS numa interrupção que vem de ring 3.

## 8. Transfira
Hoje há uma única tarefa de usuário e syscalls não reentrantes (a pilha é trocada por variáveis globais). O que mudaria para suportar várias tarefas de usuário concorrentes com preempção? (Dica: estado por-CPU via `swapgs`, uma pilha de kernel por tarefa, e o `rsp0` da TSS atualizado a cada troca.)

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário (`docs/journal/B08.md`).

## 10. Evidência e limites
Gate ENG: `B08_USERLAND_HELLO` (impresso de ring 3 via SYS_write) e `B08_USERMODE_OK` no boot, local e na CI. Limites: uma única tarefa de usuário; syscalls não reentrantes (troca de pilha por globais, sem `swapgs`/per-CPU); apenas `SYS_write` e `SYS_exit`; validação de ponteiro do usuário limitada a um teto de tamanho; o teste roda antes de habilitar interrupções, para não misturar IRQ de timer com a transição de ring.

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- Página U/S=0 em ring 3: a busca de instrução gera `#PF` com U/S=1 no código de erro; aqui o handler de #PF é fatal.
- Seletores de usuário: com STAR[63:48]=0x30, `sysret` carrega SS=0x30+8=0x38 e CS=0x30+16=0x40, ambos forçados a RPL=3 (→ 0x3b e 0x43). A ordem +8/+16 é fixada pelo hardware.
- Pilha do syscall: a do kernel, cujo topo foi gravado em `kernel_syscall_rsp` (e replicado no `rsp0` da TSS para o caso de interrupção vinda de ring 3).
- Pré-toque: a pilha de syscall está em `.bss` (NOBITS). A primeira escrita nela, se feita dentro de `syscall_entry` com interrupções mascaradas no meio da transição, dispara um `#PF` fatal; tocá-la em ring 0 antes valida/zera a página.
</details>
