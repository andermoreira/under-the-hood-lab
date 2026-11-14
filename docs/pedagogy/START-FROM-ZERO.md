# Comece do zero — primeira experiência sem programação

**Para quem:** nunca programou, nunca estudou eletrônica e quer entender como um computador funciona. Não é necessário conhecer Python, terminal ou inglês técnico para a primeira atividade.

## 1. Experimente com papel (10 minutos)

Imagine uma pequena caixa com duas entradas, A e B, cada uma podendo receber apenas **0** ou **1**. A caixa devolve **0 somente quando A e B são ambos 1**. Em todos os outros casos, devolve **1**.

Preencha antes de olhar a resposta:

| A | B | Saída da caixa |
| --- | --- | --- |
| 0 | 0 | ? |
| 0 | 1 | ? |
| 1 | 0 | ? |
| 1 | 1 | ? |

Essa caixa modela uma operação chamada **NAND**. Um **bit** é um valor 0 ou 1; **entrada** é o valor fornecido e **saída** é o resultado. Uma **tabela-verdade** enumera todos os casos possíveis.

<details><summary>Confira somente depois de tentar</summary>

As saídas, de cima para baixo, são **1, 1, 1, 0**. A regra não depende da ordem das entradas.

</details>

## 2. Descubra a inversão (10 minutos)

Agora ligue **a mesma entrada A às duas posições** da caixa NAND. Preveja o que acontece para A=0 e A=1. Confira com a regra do primeiro exercício.

Se A=0, NAND(0,0)=1. Se A=1, NAND(1,1)=0. Isso é uma operação **NOT**, ou inversão: 0 vira 1, e 1 vira 0.

**Atenção à analogia:** a caixa é um modelo lógico. Circuitos físicos têm tensão, atraso e outras características que não estamos estudando ainda.

## 3. Desafio sem copiar (10–20 minutos)

Construa a operação **AND** (saída 1 apenas quando A e B são 1), usando duas caixas NAND. Dica opcional: a primeira caixa calcula NAND(A,B); a segunda recebe duas vezes a saída da primeira.

Desenhe as duas caixas e preencha a tabela de quatro casos. Explique em uma frase por que a segunda caixa inverte o resultado da primeira.

## 4. Confira se entendeu

Sem consultar a tabela anterior, responda:

1. Quando NAND devolve 0?
2. Como obter NOT com uma NAND?
3. Como obter AND com duas NAND?
4. Qual é a diferença entre uma tabela-verdade e um circuito físico?

Se não conseguir responder, retorne ao exercício correspondente. Isso não é reprovação: é diagnóstico para escolher o próximo passo.

## 5. Próxima etapa

- Leia [F01 — bits e bytes](../foundations/F01-BITS-BYTES.md) e [F02 — lógica](../foundations/F02-LOGICA.md).
- Siga para o [Workbook A01](../workbooks/A01.md), que introduz exemplos em Python e testes automatizados. **Essa etapa exige alguma familiaridade com programação; não pule diretamente para os comandos se ainda não souber usá-los.**
- Para aprender o mínimo de terminal antes dos testes, veja [Preparação do ambiente](ENVIRONMENT.md).
- Registre o que conseguiu explicar no [diário de aprendizagem](../journal/README.md).

**Estado LEARN:** NOT_RUN. Este roteiro não foi validado com estudantes reais.
