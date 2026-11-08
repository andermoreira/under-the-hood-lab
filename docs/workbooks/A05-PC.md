# A05 — O contador de programa: qual instrução vem depois?

## Fenômeno

Uma CPU precisa guardar o endereço da próxima instrução. Em execução sequencial, esse endereço avança; em um salto, muda para outro valor; após reset, volta a zero.

**Analogia:** o marcador de página de um livro indica onde continuar a leitura.

**Limite:** o PC guarda um endereço binário, não interpreta páginas. O clock define quando o valor muda. Saltos podem substituir a sequência.

## Preveja antes de executar

Considere o PC inicialmente em zero. Preencha os resultados de cada ciclo:

| in | load | inc | reset | PC após o clock |
|---|---|---|---|---|
| 99 | 0 | 0 | 0 | ? |
| 99 | 0 | 1 | 0 | ? |
| 0x1234 | 1 | 1 | 0 | ? |
| 0 | 0 | 1 | 0 | ? |
| 0x9999 | 1 | 1 | 1 | ? |

Prioridade contratual: **reset > load > inc > hold**.

## Experimento

1. Leia `Inc16.hdl` e `PC.hdl`.
2. Execute `python3 -m unittest discover -s tests -v` para a referência Python.
3. Com o HardwareSimulator oficial instalado, execute `bash scripts/test-hdl.sh` e examine `PC.out`.
4. Compare as previsões com os resultados observados; registre o commit e os comandos.

## Refute

Troque a prioridade de `load` e `inc`. O caso em que ambos valem 1 deve revelar o erro.

## Transferência

Explique como um salto condicional na CPU pode definir `load=1` e fornecer o endereço de destino em `in`.

## Gates

ENG: implementação e testes oficiais. SCI: previsão e controle negativo. LEARN: explicar atualização por clock e prioridades sem analogia. Estado: simulador oficial PASS na CI (job `hardware-simulator`, run 42429996468, `main` @ 4f4b94d); o gate LEARN continua aberto até o registro do estudante.
