# B07 — Scheduler: escolher quem recebe a CPU

> **Escopo:** preparação conceitual para iniciante, não implementação do kernel. **ENG/SCI/LEARN:** NOT_RUN nesta alteração.

## Antes de começar

Revise a [jornada guiada](../journey/README.md), B01–B04 e o [glossário](../GLOSSARIO.md). Diferencie a CPU Hack didática do hardware x86-64; não presuma que um resultado de simulação prova comportamento em hardware real.

## 1. Problema concreto

Um atendente alterna entre filas de solicitações, preservando o ponto onde parou.

**Previsão:** como você resolveria o problema? Anote uma hipótese antes de continuar.

## 2. Modelo mental

Escalonador escolhe tarefas prontas; troca de contexto preserva estado necessário à retomada.

**Limite da analogia:** Filas humanas não modelam interrupções, privilégios, pilhas ou justiça temporal.

## 3. Experimento guiado

Trace round-robin de três tarefas A,B,C com quantum de um tick e estados ready/blocked.

Monte uma tabela com **entrada**, **estado anterior**, **ação**, **estado posterior** e **resultado esperado**. Faça a previsão antes de consultar código, logs ou respostas.

## 4. Teste negativo

Faça B bloquear antes de sua vez; qual sequência de execução seria esperada?

Especifique uma observação que refutaria sua hipótese. Não execute código privilegiado no host. Para experiências reais, use o ambiente isolado e os gates canônicos da Trilha B.

## 5. Desafio de transferência

Proponha teste para impedir que uma tarefa bloqueada seja escalonada.

Explique a solução sem analogia e identifique ao menos uma limitação. Se travar, volte ao conceito necessário; não copie uma resposta sem entender.

## 6. Verificação e diário

Registre commit, ambiente, comandos executados, resultados esperados/observados e explicação causal. Refaça a previsão em 1, 7 e 30 dias. Use a [rubrica pedagógica](../PEDAGOGICAL-AUDIT.md).

**Pendências:** exemplos resolvidos com estados intermediários, testes executáveis específicos, revisão independente e estudo com iniciantes. CI verde não significa LEARN PASS.
