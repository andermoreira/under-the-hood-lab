# B10 — Armazenamento e sistema de arquivos

> **Tipo:** roteiro pedagógico inicial. **ENG/SCI/LEARN:** NOT_RUN para este conteúdo; não declarar cobertura executável nem aprendizagem comprovada.

## Pré-requisitos

Percorra a [jornada guiada](../journey/README.md), incluindo os conceitos B01–B08, e consulte o [glossário](../GLOSSARIO.md). Esta trilha usa um kernel x86-64 próprio; **não presuma compatibilidade com syscalls Linux**.

## 1. Pergunta do mundo real

Uma biblioteca cataloga livros, mas o catálogo não é o próprio livro.

**Antes de ler:** escreva uma hipótese para o problema e o que você precisaria observar para considerá-la correta.

## 2. Conceito técnico

Blocos armazenam bytes; um sistema de arquivos mantém metadados, nomes e estruturas para localizar dados persistentes.

**Limites da analogia:** Biblioteca não modela escrita parcial, corrupção, crash consistency, cache nem dispositivos reais.

## 3. Exemplo guiado

Trace arquivo de 10 bytes dividido em blocos hipotéticos de 4 bytes: quantos blocos de dados são necessários?

Registre em uma tabela: entrada, estado inicial, transformação, resultado esperado, risco de erro. Resolva sem consultar respostas primeiro.

## 4. Teste negativo

Interrompa uma gravação antes de atualizar metadados; qual inconsistência pode surgir?

Descreva o resultado que refutaria sua hipótese. Em implementações reais, não execute imagens ou comandos não auditados no host; use ambiente isolado, testes e gates canônicos do repositório.

## 5. Transferência

Explique como detectar se dados continuam íntegros após reiniciar o emulador.

Explique a resposta sem analogia, incluindo um caso de fronteira e uma condição de falha.

## 6. Evidências e revisão

Registre commit, ambiente, hipótese, comandos realmente executados, saída observada e limites. Refaça o exercício após 1, 7 e 30 dias.

**Lacunas explícitas:** ainda faltam walkthrough executável, exemplos resolvidos passo a passo, evidência independente e piloto com iniciantes. CI de Markdown não prova execução do kernel nem LEARN PASS.
