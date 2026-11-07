# Aula A01 — Uma portaria que decide com dois sinais

## Problema

Uma portaria recebe dois sinais binários A e B. A lâmpada de saída só apaga quando os dois sinais são 1. Qual é a tabela-verdade?

## Analogia

Imagine uma regra de acesso em que a negativa só acontece quando duas condições estão simultaneamente presentes. Para todos os demais pares, a saída é 1.

## Correspondência

A e B são bits de entrada; a regra é NAND; a lâmpada representa o bit de saída.

## Onde falha

Uma portaria interpreta pessoas, regras e intenções. Uma porta NAND não interpreta nada: sua saída é função dos níveis lógicos de entrada. A analogia também não descreve atrasos elétricos.

## Preveja antes de executar

Escreva as quatro saídas para (0,0), (0,1), (1,0), (1,1). Em seguida preveja como construir NOT usando NAND.

## Construa

Implemente NOT(A)=NAND(A,A), AND(A,B)=NAND(T,T), T=NAND(A,B), e então OR e XOR apenas com NAND.

## Teste

Execute `make test`. Confira a tabela-verdade. Substitua XOR por OR deliberadamente: o caso (1,1) deve denunciar a falha.

## Explique sem analogia

Defina completude funcional, tabela-verdade e composição de portas. Explique por que NAND permite implementar outras funções booleanas.

## Recuperação ativa

Depois de 1, 7 e 30 dias, redesenhe XOR usando somente NAND sem consultar o material.
