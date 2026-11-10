# B07 — Escalonador cooperativo: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## 1. Fenômeno
Um único núcleo executa uma instrução por vez, mas o kernel precisa manter várias tarefas "no ar" ao mesmo tempo. Como é possível pausar uma função no meio, rodar outra, e mais tarde voltar exatamente de onde a primeira parou, com as variáveis locais intactas?

## 2. Previsão (preencher antes de executar)
- Quais registradores precisam ser salvos numa troca de contexto, e por que só os *callee-saved* da convenção System V AMD64 bastam quando a troca acontece dentro de uma chamada de função?
- Três tarefas A, B e C fazem três turnos cada, dando `yield` entre turnos, em round-robin começando por A. Qual é a sequência exata de letras no trace?
- O que precisa estar na pilha de uma tarefa *nova* para que o primeiro `context_switch` "retorne" para dentro dela?
- O que acontece se a função de uma tarefa simplesmente retornar em vez de dar `yield`?

## 3. Analogia
A troca de contexto é como um leitor que fecha um livro colocando um marcador na página: o `rsp` salvo é o marcador, e a pilha é o livro. Trocar de tarefa é guardar este livro com seu marcador e abrir outro no ponto marcado.

## 4. Onde a analogia falha
O "marcador" não guarda só a página: guarda também o estado dos registradores (as anotações na margem). E, diferente de um leitor humano, a CPU não "entende" o conteúdo — ela segue cegamente o `rsp`; um marcador colocado na página errada (pilha inicial mal montada) não dá "página em branco", dá *triple fault*. A analogia também esconde que não há paralelismo: só um livro é lido por vez, bem rápido.

## 5. Faça
1. Leia `kernel/x86_64/switch.S` e `kernel/x86_64/scheduler.c`, e o bloco B07 de `kmain`.
2. Desenhe a pilha inicial montada por `scheduler_spawn`: qual slot vira `r12`, qual vira o endereço de retorno?
3. Rode `make test-kernel-boot` e confira `B07_SCHEDULER_OK` e o trace `B07_SCHEDULER_TRACE_ABCABCABC`.

## 6. Refute
- Numa cópia, troque a fórmula de `next_runnable` para ignorar `from` (sempre o menor índice): preveja o novo trace e rode o boot. Qual gate falha? (Controle negativo já verificado: o boot falha com "scheduler smoke test not observed".)
- Remova um `pushq`/`popq` par em `switch.S`: o que acontece no boot e por quê?
- Faça uma tarefa nunca dar `yield`: as outras progridem? Por que isso motiva a preempção por timer (um passo futuro)?

## 7. Explique sem analogia
Explique, sem usar o livro/marcador: por que `movq %rsp, (%rdi)` salva o contexto e `movq %rsi, %rsp` o restaura; por que a ordem de `push` e `pop` precisa ser espelhada; e por que o trampolim `task_start` existe em vez de pular direto para a entrada da tarefa.

## 8. Transfira
Este escalonador é cooperativo: a tarefa decide quando ceder. O que precisaria mudar para preempção por timer (ceder no IRQ0)? Que registradores adicionais o handler de interrupção precisaria salvar que o `context_switch` cooperativo não salva, e por quê?

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário (`docs/journal/B07.md`).

## 10. Evidência e limites
Gate ENG: `B07_SCHEDULER_OK` e `B07_SCHEDULER_TRACE_ABCABCABC` no boot, local e na CI (três tarefas em round-robin determinístico, cada uma rodando até o fim). Limites: cooperativo (sem preempção); ring 0 apenas (ring 3 é o B08); pilha de uma página por tarefa, sem página de guarda; sem prioridades, sem bloqueio/sono; o loop termina quando todas as tarefas acabam, para o teste de boot não travar.

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- Salvar: `rbx, rbp, r12, r13, r14, r15`. Como a troca acontece *dentro* de uma chamada de função (`context_switch`), o compilador já tratou os *caller-saved* (`rax, rcx, rdx, rsi, rdi, r8-r11`) como voláteis antes da chamada; preservá-los seria redundante.
- Trace: `ABCABCABC` (9 letras).
- Pilha inicial (do topo p/ baixo): padding de alinhamento, endereço de `task_start` (retorno), `rbx=0`, `rbp=0`, `r12=entry`, `r13=arg`, `r14=0`, `r15=0`. O primeiro `context_switch` faz 6 `pop` e um `ret` que cai em `task_start`, que chama `entry(arg)`.
- Tarefa que retorna: `task_start` chama `scheduler_task_exited`, que marca `TASK_FINISHED` e volta ao loop; a tarefa não é mais escalonada e sua pilha é liberada.
- Transferência (preempção): o handler de IRQ0 precisaria salvar *todos* os registradores (inclusive os caller-saved e o `rip`/`rflags` que o `iretq` usa), porque a tarefa é interrompida em um ponto arbitrário, não num ponto de chamada onde o ABI já garantiu o estado.
</details>
