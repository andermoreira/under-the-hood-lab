# A03 — A ALU: a calculadora que obedece seis controles

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
