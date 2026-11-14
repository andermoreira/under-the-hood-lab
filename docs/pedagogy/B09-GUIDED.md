# B09 — ELF e carregamento de programas

> **Tipo:** roteiro pedagógico inicial. **ENG/SCI/LEARN:** NOT_RUN para este conteúdo; não declarar cobertura executável nem aprendizagem comprovada.

## Pré-requisitos

Percorra a [jornada guiada](../journey/README.md), incluindo os conceitos B01–B08, e consulte o [glossário](../GLOSSARIO.md). Esta trilha usa um kernel x86-64 próprio; **não presuma compatibilidade com syscalls Linux**.

## 1. Pergunta do mundo real

Um pacote precisa ser aberto e cada item colocado no local certo antes do uso.

**Antes de ler:** escreva uma hipótese para o problema e o que você precisaria observar para considerá-la correta.

## 2. Conceito técnico

Um loader interpreta segmentos carregáveis de ELF, mapeia memória com permissões e prepara um ponto de entrada; ELF é formato de arquivo, não garantia de execução.

**Limites da analogia:** O pacote não representa relocations, alinhamento, ABI, isolamento ou validação de arquivos malformados.

## 3. Exemplo guiado

Compare seções e segmentos: qual deles um loader normalmente usa para mapear memória em tempo de execução?

Registre em uma tabela: entrada, estado inicial, transformação, resultado esperado, risco de erro. Resolva sem consultar respostas primeiro.

## 4. Teste negativo

Imagine segmento ELF com tamanho em memória menor que tamanho em arquivo; explique por que rejeitar.

Descreva o resultado que refutaria sua hipótese. Em implementações reais, não execute imagens ou comandos não auditados no host; use ambiente isolado, testes e gates canônicos do repositório.

## 5. Transferência

Desenhe a cadeia ELF → validação → mapeamento → entrypoint e indique onde testar permissões.

Explique a resposta sem analogia, incluindo um caso de fronteira e uma condição de falha.

## 6. Evidências e revisão

Registre commit, ambiente, hipótese, comandos realmente executados, saída observada e limites. Refaça o exercício após 1, 7 e 30 dias.

**Lacunas explícitas:** ainda faltam walkthrough executável, exemplos resolvidos passo a passo, evidência independente e piloto com iniciantes. CI de Markdown não prova execução do kernel nem LEARN PASS.
