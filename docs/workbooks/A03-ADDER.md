# A03 — Como 16 bits conseguem somar?


**Pré-requisitos:** [Trilha 0](../FOUNDATIONS.md), especialmente F02–F05. Este capítulo pressupõe programação básica, não eletrônica.

## Fundamento: como o vai-um percorre uma palavra

Uma **palavra** é um grupo de bits tratado como unidade pela arquitetura. Neste circuito, a palavra tem 16 bits. Um somador de 16 bits encadeia 16 FullAdders: cada posição recebe os bits `a[i]`, `b[i]` e o carry da posição anterior. O carry inicial é zero.

**Analogia:** ao somar 099 + 001 no papel, você soma cada coluna e transporta o excedente para a próxima. **Limite:** no circuito os sinais percorrem conexões, não há uma pessoa avançando coluna por coluna; a propagação pode produzir atraso.

**Exemplo resolvido:** `0x00FF + 0x0001 = 0x0100`. Os oito bits inferiores de 0xFF são 1; adicionar 1 zera esses oito bits e transporta 1 ao nono bit.

**Exemplo de fronteira:** `0xFFFF + 0x0001 = 0x0000` em 16 bits, com carry final 1. Isso é aritmética **módulo 2¹⁶**: o resultado armazena apenas os 16 bits inferiores.

**Carry não é overflow com sinal.** Interpretando 16 bits em complemento de dois, `0x7FFF` vale 32767. Somar 1 produz `0x8000`, interpretado como -32768: houve overflow com sinal, mas não carry final. Já `0xFFFF + 1` produz carry final 1 e não representa overflow com sinal (-1 + 1 = 0).

**Experimento guiado:**
```bash
python3 - <<'PY'
for a,b in [(0xff,1),(0xffff,1),(0x7fff,1),(0x8000,0x8000)]:
    total=a+b
    result=total & 0xffff
    carry=int(total>0xffff)
    signed=lambda n: n-0x10000 if n&0x8000 else n
    overflow=int(not (-32768<=signed(a)+signed(b)<=32767))
    print(hex(a),hex(b),hex(result),"carry",carry,"overflow",overflow)
PY
```
Preveja as quatro linhas antes de executar. **Erro comum:** usar `carry` como sinônimo de overflow.


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
