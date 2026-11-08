# A03 — Como 16 bits conseguem somar?

## Fenômeno
Uma CPU com palavras de 16 bits precisa somar valores como 255 + 1 sem ter uma porta lógica especial para cada número.

**Analogia:** em uma conta de papel, cada coluna soma dois algarismos e recebe um “vai-um” da coluna anterior.

**Limites:** os bits são processados por circuitos, não por uma pessoa; propagação do carry tem atraso físico. O carry final não equivale a overflow com sinal.

## Hipótese antes da implementação
Se encadearmos 16 FullAdders, cada um recebendo o carry anterior, obteremos a soma módulo 65536.

Preveja:
- 0x00FF + 0x0001
- 0xFFFF + 0x0001
- 0x7FFF + 0x0001
- 0x8000 + 0x8000

Para cada caso, anote resultado de 16 bits, carry final e overflow **com sinal**.

## Experimento
1. Leia `hardware/nand2tetris/Add16.hdl` e trace o carry entre os bits 0 e 15.
2. Execute `python3 -m unittest discover -s tests -v`.
3. Observe os testes de fronteira e o controle negativo que remove o carry.
4. Com `N2T_HOME` configurado, rode `make test-hdl-official` e compare `Add16.out` com `Add16.cmp`.

## Desafio de transferência
Como calcular `a - b` com um somador, usando complemento de dois? Qual entrada de carry inicial seria necessária?

## Critérios
- ENG: modelo de referência testado; simulador oficial PASS na CI (job `hardware-simulator`, run 42429996468, `main` @ 4f4b94d); o gate LEARN continua aberto até o registro do estudante.
- SCI: previsões registradas e hipótese refutável.
- LEARN: explicar carry vs overflow sem recorrer à analogia.
