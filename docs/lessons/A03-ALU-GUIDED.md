# A03 — Da soma binária à ALU: aula guiada

> Público: quem completou A01–A02. Material editorial novo, **não** substitui o laboratório A03 nem atesta aprendizagem. LEARN: NOT_RUN.

## 1. O problema

Uma calculadora de 4 bits pode guardar somente 16 padrões distintos. O que acontece quando tentamos somar 15 e 1? Antes de prosseguir, escreva sua hipótese.

**Bit:** dígito 0 ou 1. **Largura:** quantidade de bits disponível. **Carry:** transporte além da posição mais alta numa soma sem sinal. **Overflow assinado:** resultado fora da faixa representável quando interpretamos os bits com sinal.

## 2. Construa com quatro bits

```text
   1111   (15 sem sinal)
 + 0001   ( 1 sem sinal)
 -------
 1 0000
 ^ ^^^^
 | 4 bits armazenados: 0000
 carry de saída: 1
```

O resultado armazenado é `0000`, pois o quinto bit não cabe. Isso **não** significa que a soma matemática de 15+1 seja zero: significa que o resultado foi truncado a quatro bits.

## 3. O mesmo padrão, outra interpretação

Em complemento de dois de 4 bits, os padrões representam de **−8 a +7**. O padrão `0111` vale +7; `0001` vale +1.

```text
  0111 (+7)
+ 0001 (+1)
-----------
  1000 (-8 se interpretado com sinal)
```

O resultado matemático +8 não cabe nessa faixa. Há **overflow assinado**, mesmo sem carry de saída.

| Operação 4 bits | Resultado | Carry | Overflow assinado |
| --- | --- | --- | --- |
| `1111 + 0001` | `0000` | 1 | 0 |
| `0111 + 0001` | `1000` | 0 | 1 |
| `1000 + 1111` | `0111` | 1 | 1 |
| `0010 + 0011` | `0101` | 0 | 0 |

Na primeira linha, `1111` representa −1 se assinado; −1+1=0, sem overflow. Na terceira, −8 + (−1) = −9, que não cabe; o resultado truncado é +7.

## 4. Observe e confira sem instalar ferramentas

Calcule cada linha à mão. Depois confira com este programa Python:

```python
cases = [(15, 1), (7, 1), (8, 15), (2, 3)]
for a, b in cases:
    total = a + b
    result = total & 0b1111
    carry = int(total > 15)
    sign_a, sign_b, sign_r = (a >> 3) & 1, (b >> 3) & 1, (result >> 3) & 1
    overflow = int(sign_a == sign_b and sign_r != sign_a)
    print(f"{a:04b}+{b:04b}={result:04b} CF={carry} OF={overflow}")
```

**Atenção:** este programa modela uma soma de 4 bits; não inspeciona flags de uma CPU física. A ALU Hack possui um contrato específico, não necessariamente os mesmos registradores de flags do x86-64.

## 5. Tente refutar

Uma pessoa diz: “Se houve carry, então houve overflow assinado”. Encontre **duas linhas** da tabela que refutam a equivalência entre carry e overflow.

## 6. Desafio sem resposta imediata

Calcule `0101 + 0101` e `1100 + 1100` em 4 bits. Para cada caso, indique resultado armazenado, carry, overflow e valor matemático assinado. Explique a diferença entre *bits resultantes* e *interpretação*.

<details><summary>Dicas graduais</summary>

1. Some os padrões como números sem sinal.
2. Guarde apenas os quatro bits menos significativos.
3. Para overflow assinado, verifique se os operandos têm o mesmo sinal e o resultado tem sinal diferente.

</details>

<details><summary>Respostas comentadas — abrir somente após tentar</summary>

- `0101+0101=1010`: 5+5=10, carry 0, overflow assinado 1; `1010` representa −6 em complemento de dois.
- `1100+1100=1000`: −4+(−4)=−8, carry 1, overflow assinado 0; −8 é representável.

</details>

## 7. Evidência e revisão

Registre sua previsão, o que errou, por que corrigiu e uma explicação sem analogia. Revise após 1, 7 e 30 dias. Testes de código não provam compreensão; use a rubrica [PACTO](../PEDAGOGY.md).

**Status:** conteúdo escrito; execução com estudante NOT_RUN; revisão independente UNVERIFIED.
