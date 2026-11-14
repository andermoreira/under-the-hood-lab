# B11 — Shell e execução de comandos

> **Tipo:** roteiro pedagógico inicial. **ENG/SCI/LEARN:** NOT_RUN para este conteúdo; não declarar cobertura executável nem aprendizagem comprovada.

## Pré-requisitos

Percorra a [jornada guiada](../journey/README.md), incluindo os conceitos B01–B08, e consulte o [glossário](../GLOSSARIO.md). Esta trilha usa um kernel x86-64 próprio; **não presuma compatibilidade com syscalls Linux**.

## 1. Pergunta do mundo real

Um atendente recebe pedidos textuais, interpreta o formato e encaminha ao serviço apropriado.

**Antes de ler:** escreva uma hipótese para o problema e o que você precisaria observar para considerá-la correta.

## 2. Conceito técnico

Shell interpreta entrada, faz parsing, resolve comandos e aciona serviços do sistema; o shell não substitui o kernel.

**Limites da analogia:** Atendente não explica quoting, processos, descritores, permissões nem erros de parsing.

## 3. Exemplo guiado

Desenhe entrada → tokenização → validação → despacho → saída para um comando fictício 'help'.

Registre em uma tabela: entrada, estado inicial, transformação, resultado esperado, risco de erro. Resolva sem consultar respostas primeiro.

## 4. Teste negativo

Insira um comando desconhecido; qual erro deve aparecer sem derrubar o shell?

Descreva o resultado que refutaria sua hipótese. Em implementações reais, não execute imagens ou comandos não auditados no host; use ambiente isolado, testes e gates canônicos do repositório.

## 5. Transferência

Defina testes de entrada vazia, espaços extras e argumento ausente.

Explique a resposta sem analogia, incluindo um caso de fronteira e uma condição de falha.

## 6. Evidências e revisão

Registre commit, ambiente, hipótese, comandos realmente executados, saída observada e limites. Refaça o exercício após 1, 7 e 30 dias.

**Lacunas explícitas:** ainda faltam walkthrough executável, exemplos resolvidos passo a passo, evidência independente e piloto com iniciantes. CI de Markdown não prova execução do kernel nem LEARN PASS.
