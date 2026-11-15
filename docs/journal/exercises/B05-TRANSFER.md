# B05 — Exercícios de transferência (sem gabarito)

> **LEARN: NOT_RUN.** Resolva sem consultar o código do PMM antes de registrar previsões. Este roteiro não é uma solução.

## Cenário 1 — Reutilização de frame

Você tem três frames livres F1, F2 e F3. Uma sequência aloca dois, libera o primeiro e aloca novamente. **Preveja** o comportamento permitido, os invariantes de unicidade e o que seria um bug. Não assuma uma política específica de seleção de frames sem consultar o código após a previsão.

## Cenário 2 — Reserva do bootloader

O kernel recebeu um mapa de memória e encontra uma região marcada como reclaimable. **Explique** sob quais condições a região pode ser reutilizada, considerando estruturas de paginação ainda referenciadas. Desenhe o fluxo da decisão.

## Cenário 3 — Controle negativo

Em branch descartável, escolha um defeito que permita entregar o mesmo frame duas vezes. Antes de alterar, indique o teste/indicador que deveria falhar. Execute e guarde log, exit code e commit; depois reverta e confirme o retorno ao verde.

## Cenário 4 — Transferência

Compare o alocador de frames B05 com `mmap` de C06: quem decide o endereço virtual, quem administra frames físicos e o que o processo Linux realmente observa? Cite duas diferenças que impeçam tratar as APIs como equivalentes.

## Rubrica para avaliação humana

- **Prever:** justificativa anterior ao teste, falsificável.
- **Construir:** modificação mínima e reversível.
- **Explicar:** frames, bitmap/estado, mapa de memória e invariantes.
- **Refutar:** defeito demonstrado com gate vermelho.
- **Transferir:** comparação tecnicamente correta B05 × C06.

Atribuir 0–3 por dimensão no diário, com justificativa do estudante e revisão independente. **Não registrar aprovação automática.**
