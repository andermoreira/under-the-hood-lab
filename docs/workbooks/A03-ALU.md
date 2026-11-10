# A03 — A ALU: a calculadora que obedece seis controles


**Pré-requisitos:** [Trilha 0](../FOUNDATIONS.md), especialmente F02–F05. Este capítulo pressupõe programação básica, não eletrônica.

## Fundamento: uma calculadora configurável

**ALU** significa unidade lógica e aritmética. Ela recebe operandos `x` e `y`, sinais de controle e produz `out` e flags. A ALU Hack usa seis bits de controle: `zx` zera x, `nx` inverte x, `zy` zera y, `ny` inverte y, `f` seleciona AND (0) ou soma (1), e `no` inverte a saída. A ordem dessas transformações é parte da especificação.

**Analogia:** uma máquina de cozinha tem seletores que alteram o preparo antes de executar a operação principal. **Limite:** a ALU não movimenta peças ou ingredientes; seus controles atuam sobre sinais e circuitos.

**Exemplo resolvido:** para x=1 e y=1, com `zx=nx=zy=ny=no=0`, `f=0` produz `1 AND 1 = 1`; `f=1` produz `1+1=2`. A diferença é visível mesmo sem compreender os demais controles.

**Flags:** `zr=1` quando os 16 bits de `out` são zero. `ng` copia o bit mais significativo de `out`, interpretado como sinal na representação em complemento de dois. `ng=1` não significa que houve erro.

**Caso-limite:** para x=0, y=0, AND e soma produzem ambos zero. Um teste apenas com zeros **não detecta** troca acidental do controle `f`.

**Experimento independente:**
```bash
python3 - <<'PY'
for x,y in [(0,0),(1,1),(1,2),(0xffff,1)]:
    print(hex(x),hex(y),"AND",hex(x&y),"ADD",hex((x+y)&0xffff))
PY
```
Preveja os resultados e depois localize os controles correspondentes em `ALU.hdl`. **Erro comum:** confundir o bit `ng` com carry ou com a comparação entre operandos.


## Fenômeno
Uma mesma rede de circuitos produz soma, AND, OR, negação e outras operações sem precisar de uma máquina separada para cada tarefa.

**Analogia:** uma bancada de trabalho com seis seletores muda como os materiais passam pelas ferramentas.

**Limite:** não existem ferramentas físicas móveis dentro da ALU; são sinais elétricos que selecionam caminhos combinacionais.

## Preveja
Para x=1, y=1, compare f=0 (AND) e f=1 (ADD), mantendo zx=nx=zy=ny=no=0. Qual é o resultado?

Explique a diferença entre a saída `out`, a flag `zr` (resultado zero) e a flag `ng` (bit de sinal).

## Experimente
- Leia `ALU.hdl` da esquerda para a direita: normalização de x e y, escolha da operação, negação opcional e flags.
- Rode `make verify` para validar o modelo Python de referência.
- Rode `make test-hdl-official` quando o simulador oficial estiver disponível.

## Refute
Inverta o controle f. Quais entradas distinguem AND de ADD? Um teste que usa apenas zeros conseguiria detectar a troca?

## Transferência
Por que a ALU consegue calcular x-y usando complemento de dois mesmo sem um circuito de subtração separado?

## Evidência
Testes de referência Python não comprovam o HDL. Registre execução do simulador oficial, stdout, exit code e comparação .cmp. Status: simulador oficial PASS na CI (job `hardware-simulator`, run 42429996468, `main` @ 4f4b94d); o gate LEARN continua aberto até o registro do estudante.
