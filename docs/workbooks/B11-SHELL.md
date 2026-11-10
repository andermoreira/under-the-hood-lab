# B11 — Shell do kernel: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## 1. Fenômeno
Até agora o kernel executava uma sequência fixa de testes. Um sistema utilizável recebe comandos e reage. Como transformar uma linha de texto como `cat greeting.txt` em uma ação (ler um arquivo do disco e imprimi-lo), ligando teclado/entrada, sistema de arquivos e carregador de programas?

## 2. Previsão (preencher antes de executar)
- Como separar `run hello` em "comando" e "argumento" sem uma biblioteca de strings?
- Quando o shell faz `run hello`, que subsistemas dos módulos anteriores entram em ação, e em que ordem?
- Por que o shell reaproveita o mesmo parser que um editor de linha ligado ao teclado usaria?
- O que deve acontecer com um comando desconhecido?

## 3. Analogia
O shell é um recepcionista: lê um pedido escrito, identifica a palavra-chave, e encaminha ao setor certo (arquivos, programas) sem executar o trabalho ele mesmo.

## 4. Onde a analogia falha
O "recepcionista" não tem bom senso: só reconhece exatamente as palavras programadas, e um pedido malformado não é "interpretado com boa vontade" — ou casa um built-in, ou é rejeitado. Ele também roda no mesmo nível de privilégio que tudo (ring 0): não há separação entre o recepcionista e a diretoria.

## 5. Faça
1. Leia `kernel/x86_64/shell.c` (parser `tokenize`, dispatch em `shell_exec`) e o `shell_selftest`.
2. Rode `make test-kernel-boot` e confirme `B11_LS_greeting.txt` e `B11_SHELL_OK`.
3. Siga `run hello`: `elf_load` → `paging_map_user_page` → `usermode_run`.

## 6. Refute
- Numa cópia, remova o caso `"cat"` do dispatch: o que o shell responde a `cat greeting.txt`?
- Dê um argumento a mais a `write`: o parser (máximo 3 tokens) lida bem?
- Rode `run inexistente`: o shell distingue de `run hello`?

## 7. Explique sem analogia
Explique sem o recepcionista: como `tokenize` transforma espaços em terminadores nulos in-place, por que `run hello` precisa liberar (unmap) as páginas de usuário entre execuções do mesmo ELF `ET_EXEC`, e por que o shell roda em ring 0.

## 8. Transfira
Hoje os comandos vêm de um script fixo. Como ligar o teclado PS/2 (B04) a um editor de linha que alimenta `shell_exec`? O que muda quando a entrada é assíncrona (IRQ) em vez de um array?

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário (`docs/journal/B11.md`).

## 10. Evidência e limites
Gate ENG: `B11_LS_greeting.txt` e `B11_SHELL_OK` no boot, local e na CI (o shell lista, lê o disco, e roda dois programas de usuário). Limites: comandos vêm de um script fixo (entrada por teclado é refinamento futuro); built-ins mínimos (`ls`, `cat`, `write`, `run`); shell roda em ring 0; `ls` conhece o diretório plano semeado.

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- Separar: varrer a linha trocando espaços por `\0` e guardando o início de cada token (parser in-place, sem alocação).
- `run hello` aciona, em ordem: carregador ELF (B09) → mapeamento de página de usuário (B08) → entrada em ring 3 via SYSRET (B08) → syscalls do programa.
- Comando desconhecido: emite `B11_CMD_UNKNOWN`, não executa nada — falhar explícito é melhor que adivinhar.
</details>
