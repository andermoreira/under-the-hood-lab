# Auditoria pré-merge — PR #31

**Head auditado:** `d272897322e8adcad769e96c30ca3d4c570309dd` (antes da inclusão deste relatório). **Base:** `main` em `9e619a296aa5e3f9d5e17e2c208f8a93d4939836`. **Data:** 2026-11-10.

## Escopo verificado

- GitHub informa PR aberta, Draft, mergeable=true, 30 arquivos alterados, 54 commits no momento da consulta.
- Foram lidos os arquivos de conteúdo via GitHub e inspecionados programaticamente os 27 capítulos (8 F, 7 A, 12 B).
- **PASS (inspeção estática pontual):** cada um dos 27 capítulos contém exatamente um bloco `mermaid`; o número de delimitadores Markdown de código é par; há menção explícita a limites de analogia e exemplos/experimentos.
- **PASS (inspeção estática pontual):** os 8 capítulos F contêm `NOT_RUN` e não simulam conclusão da aprendizagem.
- **PASS (metadados GitHub):** nenhum review de PR registrado no momento da consulta.
- **NOT_RUN:** execução real de `python3 -m unittest discover -s tests -v` e demais gates. Tentativa de clonar o repositório para execução local falhou por DNS do ambiente (`Could not resolve host: github.com`). Isso **não é** falha do código.
- **NOT_RUN:** renderização real dos Mermaid no GitHub; a inspeção de fences não é validação de parser/renderização.
- **NOT_RUN:** avaliação independente com leitor iniciante, exercícios sem consulta, medição de aprendizagem e revisão espaçada.
- **UNVERIFIED:** precisão de todos os comandos e caminhos dos capítulos F03–F08, que não foram comparados exaustivamente com a árvore do repositório.
- **UNVERIFIED:** evidências históricas de CI reproduzidas nos workbooks originais, pois não foram reexecutadas neste head.

## Pendências que bloqueiam aprovação

1. Executar os testes no commit final, com logs e status de saída registrados.
2. Validar renderização de todos os 27 diagramas e corrigir qualquer erro de Mermaid.
3. Conferir caminhos/comandos contra o repositório e executar ao menos um experimento por trilha.
4. Revisar profundidade e gabaritos: os guias novos da Trilha B acrescentam exercícios, mas **não substituem** gabaritos resolvidos de cada questão. A rubrica exige dois exemplos resolvidos; isso ainda não foi comprovado para todos os capítulos.
5. Obter revisão independente de alguém que não escreveu o conteúdo, preferencialmente com o perfil de estudante-alvo.
6. Atualizar a decisão somente após evidências; `mergeable=true` indica ausência de conflito detectado pelo GitHub, não qualidade ou CI aprovado.

## Decisão

**NÃO LIBERADO PARA MERGE (NOT_RUN/UNVERIFIED).** A inspeção estática passou nos critérios limitados acima, mas não satisfaz o contrato pedagógico completo. A PR deve permanecer Draft. A decisão pode mudar após completar os gates e registrar evidências.
