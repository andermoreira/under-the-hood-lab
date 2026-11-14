# A05 — CPU Hack: seguindo o endereço da próxima instrução

> Aula complementar para iniciantes. Pressupõe A01–A04. O modelo é didático; LEARN NOT_RUN.

## 1. Pergunta concreta
Ao ler uma receita, você sabe qual passo vem depois. Mas como uma CPU decide qual instrução executar após um salto?

**PC (Program Counter)** é o registrador que indica o endereço da instrução a buscar. **Instrução** é um comando codificado da ISA. **Salto** altera a sequência normal de endereços.

**Analogia:** um marcador de página aponta o próximo passo. **Limite:** CPUs reais têm detalhes de pipeline, temporização e exceções; o modelo Hack tem sua própria semântica de PC.

## 2. Exemplo resolvido: fluxo sem salto

No modelo simplificado, se a instrução não desvia, o PC avança uma posição:

| Ciclo | PC antes | Instrução abstrata | PC depois |
| --- | --- | --- | --- |
| 1 | 0 | atribuição | 1 |
| 2 | 1 | atribuição | 2 |
| 3 | 2 | atribuição | 3 |

Essas são **instruções abstratas**, não bytes reais da ISA Hack. Para a CPU Hack, consulte a especificação de A-instruction/C-instruction e condições de jump.

## 3. Preveja antes de consultar

Programa abstrato: endereço 0 avança; endereço 1 salta para 4; endereço 4 avança; endereço 5 salta para 1. Preencha os PCs visitados em seis ciclos.

<details><summary>Dica progressiva</summary>

Em cada ciclo, registre o PC atual. Depois escolha entre PC+1 ou endereço de destino.

</details>

<details><summary>Resposta comentada</summary>

PCs: 0, 1, 4, 5, 1, 4. O salto em 5 forma um laço.

</details>

## 4. Experimento reproduzível (modelo abstrato)

```python
pc = 0
jumps = {1: 4, 5: 1}
for cycle in range(6):
    print(f"ciclo={cycle + 1} pc={pc}")
    pc = jumps.get(pc, pc + 1)
```

Antes de executar, preveja as seis linhas. Esse código **não é um simulador da CPU Hack**; serve apenas para observar seleção de próximo endereço.

## 5. Teste negativo e transferência

**Falha controlada:** altere `jumps = {1: 4, 5: 1}` para `{1: 4, 5: 2}`. Em qual ciclo a sequência diverge? Resposta: no sexto, quando PC passa a 2 em vez de 1.

**Desafio novo:** desenhe um fluxo abstrato que visita 0, 1, 3, 4, 3, 4. Defina os saltos necessários. Depois explique como distinguir **endereço** de **valor armazenado no endereço**.

## 6. Conexão com o laboratório

Inspecione o capítulo A05 e a implementação de PC/CPU Hack da Trilha A. Compare o modelo abstrato com o comportamento real do hardware, inclusive reset, load e increment. Não trate equivalência como demonstrada sem executar os testes correspondentes.

Registre previsões, resultado observado, erro corrigido e explicação sem analogia. Revise em 1, 7 e 30 dias. **ENG/SCI/LEARN: não executados nesta PR editorial.**
