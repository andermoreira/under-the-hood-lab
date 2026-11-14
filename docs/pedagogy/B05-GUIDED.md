# B05 — Alocação física: de frames livres à memória utilizável

> **Escopo:** preparação conceitual para iniciante, não implementação do kernel. **ENG/SCI/LEARN:** NOT_RUN nesta alteração.

## Antes de começar

Revise a [jornada guiada](../journey/README.md), B01–B04 e o [glossário](../GLOSSARIO.md). Diferencie a CPU Hack didática do hardware x86-64; não presuma que um resultado de simulação prova comportamento em hardware real.

## 1. Problema concreto

Um estacionamento tem vagas ocupadas, livres e reservadas.

**Previsão:** como você resolveria o problema? Anote uma hipótese antes de continuar.

## 2. Modelo mental

Frame é uma unidade de memória física gerenciada pelo alocador; o mapa de memória do bootloader informa regiões utilizáveis ou reservadas.

**Limite da analogia:** Uma vaga não representa alinhamento, endereços físicos, DMA ou memória defeituosa.

## 3. Experimento guiado

Num mapa hipotético de oito frames com estados R,L,L,R,L,R,L,L, escolha dois frames livres sem usar reservados.

Monte uma tabela com **entrada**, **estado anterior**, **ação**, **estado posterior** e **resultado esperado**. Faça a previsão antes de consultar código, logs ou respostas.

## 4. Teste negativo

Marque um frame reservado como livre; qual teste de segurança do alocador deve rejeitar a seleção?

Especifique uma observação que refutaria sua hipótese. Não execute código privilegiado no host. Para experiências reais, use o ambiente isolado e os gates canônicos da Trilha B.

## 5. Desafio de transferência

Desenhe um algoritmo de first-fit e diga quando retorna falha.

Explique a solução sem analogia e identifique ao menos uma limitação. Se travar, volte ao conceito necessário; não copie uma resposta sem entender.

## 6. Verificação e diário

Registre commit, ambiente, comandos executados, resultados esperados/observados e explicação causal. Refaça a previsão em 1, 7 e 30 dias. Use a [rubrica pedagógica](../PEDAGOGICAL-AUDIT.md).

**Pendências:** exemplos resolvidos com estados intermediários, testes executáveis específicos, revisão independente e estudo com iniciantes. CI verde não significa LEARN PASS.
