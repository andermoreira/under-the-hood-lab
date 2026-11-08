# A05 — A CPU Hack: de circuitos a instruções

## Problema
Como uma sequência de 16 bits decide se a CPU deve guardar um número, calcular, escrever na memória ou saltar?

**Analogia:** uma central de triagem recebe um cartão com campos que determinam o destino e a operação.

**Limite:** a CPU não “lê” um cartão semanticamente; bits controlam diretamente multiplexadores, registradores, ALU e PC.

## Preveja
- `@7` carrega A com 7 e incrementa PC.
- `D=A` copia o valor de A para D.
- `@5`, seguido de `D=D+A`, produz D=12.
- `0;JMP` carrega no PC o endereço que A guardava **antes** da borda do clock.
- Uma instrução A nunca deve ativar `writeM`.

## Experimente
1. Leia `CPU.hdl` e identifique `instruction[15]` (A ou C).
2. Identifique `a`, `comp`, `dest` e `jump` no formato C.
3. Rode `python3 -m unittest discover -s tests -v` para validar o modelo Python de referência.
4. Rode `bash scripts/test-hdl.sh` com o simulador oficial e compare os vetores CPU.

## Refute
Altere a condição `JGT` para sempre saltar. O teste `0;JGT` deve denunciar a falha.

## Transferência
Explique por que o endereço de salto vem do registrador A e por que a escrita em M é um sinal de saída para a memória externa, não uma RAM dentro da CPU.

## Evidência
O modelo Python não prova a correção do HDL. ENG, SCI e LEARN são gates distintos. Estado: simulador oficial PASS na CI (job `hardware-simulator`, run 42429996468, `main` @ 4f4b94d); o gate LEARN continua aberto até o registro do estudante.
