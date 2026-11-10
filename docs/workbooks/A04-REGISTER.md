# A04 — O circuito que lembra


**Pré-requisitos:** [Trilha 0](../FOUNDATIONS.md), especialmente F02–F05. Este capítulo pressupõe programação básica, não eletrônica.

## Fundamento: o que significa guardar um bit?

Uma porta combinacional calcula a partir das entradas atuais; um **elemento de estado** preserva informação entre instantes. O DFF (flip-flop tipo D) captura um valor na transição definida de relógio do modelo. Um **registrador** combina vários elementos de estado; um MUX pode decidir se a próxima atualização recebe o novo valor ou conserva o anterior.

**Analogia:** um quadro de avisos só é substituído quando chega uma autorização de atualização. **Limite:** um registrador é volátil e seu comportamento depende de eventos de relógio; não é uma anotação permanente.

**Exemplo resolvido:** estado inicial 0, entrada 1, `load=1`: depois da atualização, estado 1. Em seguida, entrada 0, `load=0`: depois da atualização, estado **continua 1**. Só com `load=1` o novo zero será capturado.

| Estado anterior | in | load | Próximo estado |
|---|---|---|---|
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 |

**Experimento independente:**
```bash
python3 - <<'PY'
state=0
for value,load in [(1,1),(0,0),(0,1),(1,0)]:
    state=value if load else state
    print("in",value,"load",load,"state",state)
PY
```
Preveja cada linha. **Erro comum:** achar que mudar `in` muda imediatamente o estado armazenado. O modelo Python simplifica o relógio; o teste HDL deve verificar a semântica de `tick/tock`.


## Fenômeno

Uma porta combinacional responde às entradas atuais. Um registrador precisa **manter um valor** mesmo quando a entrada muda.

**Analogia:** um quadro branco conserva a última anotação até alguém autorizar uma substituição.

**Limites:** o registrador armazena estado elétrico e é atualizado por eventos de clock; não é um objeto passivo nem uma memória permanente.

## Hipótese

Um `DFF` conserva o último valor amostrado. Com um `Mux` que escolhe entre o valor anterior e a nova entrada, o sinal `load` controla se haverá atualização.

Preveja a saída após cada ciclo:

| in | load | saída prevista |
|---|---|---|
| 0 | 0 | ? |
| 1 | 1 | ? |
| 0 | 0 | ? |
| 0 | 1 | ? |
| 1 | 0 | ? |

## Experimento

1. Examine `Bit.hdl` e identifique o laço de realimentação por meio do DFF.
2. Execute `python3 -m unittest discover -s tests -v` para o modelo Python.
3. Com o HardwareSimulator oficial disponível, execute `bash scripts/test-hdl.sh` e compare `Bit.out` e `Register.out`.
4. Registre o comportamento após `tick, tock`; não confunda estado anterior com o próximo estado.

## Refutação

Remova o controle `load` e escreva sempre. O teste que tenta preservar `0x1234` quando `in=0xffff` deve falhar.

## Transferência

Por que 16 bits de memória exigem 16 elementos de estado, mas podem compartilhar o mesmo sinal de `load`?

## Evidência

O modelo Python não comprova a temporização do HDL. Gates separados: ENG, SCI, LEARN. Estado: simulador oficial PASS na CI (job `hardware-simulator`, run 42429996468, `main` @ 4f4b94d); o gate LEARN continua aberto até o registro do estudante.
