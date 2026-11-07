# Guia do iniciante — seu primeiro circuito em 15 minutos

## A pergunta
Como uma máquina toma uma decisão com apenas 0 e 1?

Imagine uma **portaria com dois sinais**. Uma lâmpada permanece acesa (1) em quase todas as combinações; apaga (0) apenas quando A e B estão ambos ligados. Esse é o comportamento NAND.

| A | B | NAND |
|---|---|---|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

### Onde a analogia falha
Uma portaria interpreta regras e pessoas. Uma porta NAND não interpreta: implementa uma função booleana, com sinais físicos e atraso de propagação.

## Faça uma previsão
Sem consultar código: qual será a saída de NAND(1,1)? Como você inverteria um bit usando só NAND?

## Execute
```sh
make test
```
O comando valida um **modelo lógico Python**, não um circuito elétrico nem HDL do Nand2Tetris.

## Descubra
NOT(A) = NAND(A,A). Você consegue construir AND e OR sem usar outras primitivas?

## Explique sem analogia
Defina tabela-verdade, completude funcional e por que duas entradas ligadas produzem saída 0.

## Se falhar
- `python3: command not found`: instale Python 3.
- `make: command not found`: instale Make ou execute `python3 -m unittest discover -s tests -v`.
- Erro de importação: execute na raiz do repositório.

## Depois
Abra [o workbook A01](workbooks/A01.md) e registre sua própria resposta.
