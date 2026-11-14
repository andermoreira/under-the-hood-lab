# B12 — Integração e capstone: boot até recuperação

> **Tipo:** roteiro pedagógico inicial. **ENG/SCI/LEARN:** NOT_RUN para este conteúdo; não declarar cobertura executável nem aprendizagem comprovada.

## Pré-requisitos

Percorra a [jornada guiada](../journey/README.md), incluindo os conceitos B01–B08, e consulte o [glossário](../GLOSSARIO.md). Esta trilha usa um kernel x86-64 próprio; **não presuma compatibilidade com syscalls Linux**.

## 1. Pergunta do mundo real

Uma viagem só está completa quando cada conexão funciona e o viajante chega ao destino.

**Antes de ler:** escreva uma hipótese para o problema e o que você precisaria observar para considerá-la correta.

## 2. Conceito técnico

Um teste de integração verifica contratos entre boot, memória, scheduler, modo usuário, I/O e persistência; sucesso isolado de módulos não comprova o sistema completo.

**Limites da analogia:** Viagem não modela falhas de concorrência, durabilidade nem comportamento não determinístico.

## 3. Exemplo guiado

Monte uma matriz: boot, iniciar dois programas, isolar memória, gravar arquivo, reiniciar, ler arquivo.

Registre em uma tabela: entrada, estado inicial, transformação, resultado esperado, risco de erro. Resolva sem consultar respostas primeiro.

## 4. Teste negativo

Injete falha de leitura após reboot e identifique quais evidências isolam armazenamento de shell.

Descreva o resultado que refutaria sua hipótese. Em implementações reais, não execute imagens ou comandos não auditados no host; use ambiente isolado, testes e gates canônicos do repositório.

## 5. Transferência

Especifique evidências mínimas para ENG e SCI e explique por que LEARN exige avaliação humana.

Explique a resposta sem analogia, incluindo um caso de fronteira e uma condição de falha.

## 6. Evidências e revisão

Registre commit, ambiente, hipótese, comandos realmente executados, saída observada e limites. Refaça o exercício após 1, 7 e 30 dias.

**Lacunas explícitas:** ainda faltam walkthrough executável, exemplos resolvidos passo a passo, evidência independente e piloto com iniciantes. CI de Markdown não prova execução do kernel nem LEARN PASS.
