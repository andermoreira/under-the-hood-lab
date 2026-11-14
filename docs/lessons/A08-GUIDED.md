# A08 — Como um programa multiplica somando

> Aula complementar. Pressupõe A05–A07. LEARN NOT_RUN.

## 1. Pergunta

Se você só pudesse somar, comparar e saltar, como calcular 3×4?

**Laço:** sequência repetida até uma condição de parada. **Acumulador:** valor atualizado a cada repetição. **Invariante:** propriedade que continua verdadeira ao longo das iterações.

**Analogia:** colocar quatro grupos de três objetos numa caixa. **Limite:** um programa precisa de estado, condição de parada e regras explícitas para entradas e limites numéricos.

## 2. Exemplo resolvido

Queremos `3 × 4`. Começamos com `acc=0` e `count=0`. A cada passo, somamos 3 e aumentamos o contador.

| Iteração | acc | count |
| --- | --- | --- |
| Inicial | 0 | 0 |
| 1 | 3 | 1 |
| 2 | 6 | 2 |
| 3 | 9 | 3 |
| 4 | 12 | 4 |

A cada passo vale a **invariante** `acc = 3 × count`. Quando `count=4`, `acc=12`.

## 3. Preveja e execute

```python
a, b = 3, 4
acc, count = 0, 0
while count < b:
    acc += a
    count += 1
    print(f"count={count} acc={acc}")
assert acc == a * b
```

Preveja cada linha antes de executar. O exemplo Python demonstra o algoritmo, não o encoding Hack nem o custo de execução da CPU.

## 4. Falha controlada

Troque `count < b` por `count <= b`. Qual resultado aparece? A execução faz cinco somas e retorna 15, divergindo do esperado 12. Registre a falha e restaure o operador.

## 5. Casos de fronteira

- `a=0, b=4`: quatro somas de zero, resultado zero.
- `a=3, b=0`: nenhuma soma, resultado zero.
- `a=1, b=1`: uma soma, resultado um.

**Limite:** o algoritmo acima pressupõe `b >= 0`. Não trata operandos negativos, overflow de palavra de 16 bits ou entradas inválidas. A implementação Hack precisa definir explicitamente tais casos.

## 6. Transferência

Sem copiar o exemplo, escreva um algoritmo que calcule `5 × 3` usando três somas e explique sua invariante. Depois proponha um teste que detecte um erro de parada antecipada.

<details><summary>Resposta comentada</summary>

Comece com acc=0, count=0. Após três iterações, acc=15 e count=3. A invariante é acc=5×count. Um erro de parada antecipada produz 10, detectável pelo teste esperado 15.

</details>

## 7. Conexão com a CPU Hack

Traduza a ideia de acumulador, contador, comparação e salto para instruções Hack usando o capítulo A07. Não assuma que o código Python é executável diretamente na CPU Hack.

Registre o trace e explique a invariante sem analogia. Revise em 1, 7 e 30 dias. **ENG/SCI/LEARN: não executados nesta PR editorial.**
