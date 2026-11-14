# A04 — Estado, clock e registradores: aula guiada

> Público: quem completou A01–A03. Material editorial complementar. LEARN: NOT_RUN.

## 1. O problema

Uma porta NAND isolada produz saída que depende das entradas atuais. Mas como um computador **lembra** um valor depois que a entrada muda?

Precisamos distinguir **lógica combinacional** (saída depende das entradas atuais) de **lógica sequencial** (saída depende também do estado guardado).

## 2. Analogia e limite

Imagine um quadro que só é atualizado quando toca um sinal. O quadro representa o valor guardado; o sinal representa o evento de atualização.

**Limite:** um circuito real não “ouve” um sino. Sinais elétricos possuem tempos de propagação, requisitos de setup/hold e podem sofrer metastabilidade. O modelo abaixo é idealizado.

## 3. Modelo de registrador de um bit

Um registrador possui entrada `D`, saída atual `Q`, sinal `load` e uma borda ativa do clock.

Na borda: se `load=1`, o próximo estado `Q'` recebe `D`; caso contrário, `Q'=Q`. Fora da borda, neste modelo, `Q` permanece constante.

| Antes da borda Q | Entrada D | load | Depois da borda Q' |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 |

**Pergunta de previsão:** se `D` muda entre bordas, o que acontece com `Q` neste modelo?

## 4. Experimento guiado

Considere `Q=0` inicialmente. Em cada linha, aplique a entrada na próxima borda:

| Borda | D | load | Preveja Q depois |
| --- | --- | --- | --- |
| 1 | 1 | 1 | ? |
| 2 | 0 | 0 | ? |
| 3 | 0 | 1 | ? |
| 4 | 1 | 0 | ? |
| 5 | 1 | 1 | ? |

Faça o trace manual antes de conferir.

<details><summary>Respostas — confira após tentar</summary>

Após cada borda: 1, 1, 0, 0, 1. Nas bordas 2 e 4, `load=0` preserva o estado.

</details>

## 5. Verifique com modelo executável

```python
q = 0
events = [(1, 1), (0, 0), (0, 1), (1, 0), (1, 1)]
for edge, (d, load) in enumerate(events, start=1):
    if load:
        q = d
    print(f"borda={edge} D={d} load={load} Q={q}")
```

Este modelo em Python simula **transições discretas**; não simula atrasos elétricos, setup/hold ou implementação de flip-flops.

## 6. Falha controlada

Mude a condição `if load:` para `if not load:`. Preveja a primeira borda em que o modelo defeituoso diverge da tabela. Execute somente em uma cópia temporária e restaure depois.

## 7. Transferência

Projete um registrador de **dois bits** com `load` compartilhado. Estado inicial `00`. Entradas por borda: `(11,1)`, `(01,0)`, `(10,1)`. Registre o estado após cada borda e explique por que os dois bits mudam juntos no modelo.

<details><summary>Dica</summary>

Trate o valor de dois bits como uma unidade: só substitua o estado quando `load=1`.

</details>

<details><summary>Resposta comentada</summary>

Estados: `11`, `11`, `10`. Na segunda borda, `load=0` preserva ambos os bits.

</details>

## 8. Conexão e avaliação

Relacione o modelo à implementação de registradores na Trilha A; não assuma que o código Python substitui os testes HDL oficiais. Explique o que é estado, quando ele muda e qual caso negativo evidencia erro de `load`. Revise após 1, 7 e 30 dias.

**Status:** conteúdo escrito; execução com estudante NOT_RUN; revisão independente UNVERIFIED.
