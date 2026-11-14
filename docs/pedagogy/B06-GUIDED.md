# B06 — Paginação e memória virtual: endereço não é localização física

> **Escopo:** preparação conceitual para iniciante, não implementação do kernel. **ENG/SCI/LEARN:** NOT_RUN nesta alteração.

## Antes de começar

Revise a [jornada guiada](../journey/README.md), B01–B04 e o [glossário](../GLOSSARIO.md). Diferencie a CPU Hack didática do hardware x86-64; não presuma que um resultado de simulação prova comportamento em hardware real.

## 1. Problema concreto

Um hotel entrega números de quarto aos hóspedes, mas pode reorganizar a ocupação interna.

**Previsão:** como você resolveria o problema? Anote uma hipótese antes de continuar.

## 2. Modelo mental

Paginação traduz endereços virtuais em físicos por tabelas; permissões limitam leitura, escrita e execução.

**Limite da analogia:** Quartos não explicam TLB, page fault, tamanhos de página ou isolamento entre espaços de endereços.

## 3. Experimento guiado

Com páginas hipotéticas de 4096 bytes, separe endereço virtual 0x2005 em índice de página e offset.

Monte uma tabela com **entrada**, **estado anterior**, **ação**, **estado posterior** e **resultado esperado**. Faça a previsão antes de consultar código, logs ou respostas.

## 4. Teste negativo

Remova o mapeamento da página 2 e preveja a condição de page fault ao acessar 0x2005.

Especifique uma observação que refutaria sua hipótese. Não execute código privilegiado no host. Para experiências reais, use o ambiente isolado e os gates canônicos da Trilha B.

## 5. Desafio de transferência

Compare duas tabelas de páginas que mapeiam o mesmo virtual para frames diferentes.

Explique a solução sem analogia e identifique ao menos uma limitação. Se travar, volte ao conceito necessário; não copie uma resposta sem entender.

## 6. Verificação e diário

Registre commit, ambiente, comandos executados, resultados esperados/observados e explicação causal. Refaça a previsão em 1, 7 e 30 dias. Use a [rubrica pedagógica](../PEDAGOGICAL-AUDIT.md).

**Pendências:** exemplos resolvidos com estados intermediários, testes executáveis específicos, revisão independente e estudo com iniciantes. CI verde não significa LEARN PASS.
