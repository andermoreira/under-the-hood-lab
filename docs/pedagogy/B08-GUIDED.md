# B08 — Ring 3 e syscalls: atravessando a fronteira de privilégio

> **Escopo:** preparação conceitual para iniciante, não implementação do kernel. **ENG/SCI/LEARN:** NOT_RUN nesta alteração.

## Antes de começar

Revise a [jornada guiada](../journey/README.md), B01–B04 e o [glossário](../GLOSSARIO.md). Diferencie a CPU Hack didática do hardware x86-64; não presuma que um resultado de simulação prova comportamento em hardware real.

## 1. Problema concreto

Uma pessoa solicita um serviço ao balcão em vez de entrar na sala de máquinas.

**Previsão:** como você resolveria o problema? Anote uma hipótese antes de continuar.

## 2. Modelo mental

Modo usuário tem privilégios limitados; syscall faz transição controlada para serviço do kernel.

**Limite da analogia:** Balcão não descreve MSRs, ABI, pilhas, validação de ponteiros nem transições reais.

## 3. Experimento guiado

Desenhe programa usuário → wrapper → entrada syscall → validação → kernel → retorno.

Monte uma tabela com **entrada**, **estado anterior**, **ação**, **estado posterior** e **resultado esperado**. Faça a previsão antes de consultar código, logs ou respostas.

## 4. Teste negativo

Passe um ponteiro inválido hipotético; explique por que o kernel deve rejeitá-lo sem confiar na origem.

Especifique uma observação que refutaria sua hipótese. Não execute código privilegiado no host. Para experiências reais, use o ambiente isolado e os gates canônicos da Trilha B.

## 5. Desafio de transferência

Compare a ABI de syscalls do kernel próprio com a Linux, sem presumir compatibilidade.

Explique a solução sem analogia e identifique ao menos uma limitação. Se travar, volte ao conceito necessário; não copie uma resposta sem entender.

## 6. Verificação e diário

Registre commit, ambiente, comandos executados, resultados esperados/observados e explicação causal. Refaça a previsão em 1, 7 e 30 dias. Use a [rubrica pedagógica](../PEDAGOGICAL-AUDIT.md).

**Pendências:** exemplos resolvidos com estados intermediários, testes executáveis específicos, revisão independente e estudo com iniciantes. CI verde não significa LEARN PASS.
