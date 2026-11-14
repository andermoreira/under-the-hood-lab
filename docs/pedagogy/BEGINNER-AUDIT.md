# Auditoria de entrada para autodidatas — 2026-11-14

> Escopo: leitura documental amostral da jornada, guia iniciante, workbook A01, glossário, método PACTO, contrato de qualidade e C01. **Não** é um estudo com alunos. ENG, SCI e LEARN permanecem independentes.

## Achados com evidência

| Achado | Evidência | Gravidade | Ação |
| --- | --- | --- | --- |
| A01 já tem boa estrutura de ensino | `docs/workbooks/A01.md`: fenômeno, analogia e limites, três exemplos resolvidos, mutação, transferência, revisão espaçada | Ponto forte | Preservar, não reescrever do zero |
| Público presumido não é iniciante absoluto | Workbook A01: “sabe programar”; analogia de função pura e trecho Python | Alta | Oferecer rota sem programação prévia |
| Primeiro contato exige ferramentas antes de explicar instalação | `docs/INICIANTE.md`: `make test` e dicas de erro; faltam passos de instalação por sistema e checagem | Alta | Adicionar percurso manual sem terminal e roteiro de preparação |
| Perguntas de previsão usam termos que podem ser novos | Guia iniciante: inverter bit; workbook: XOR e mutação | Média | Dividir previsões em iniciante e extensão, fornecer explicação progressiva |
| Jornada mistura duas interpretações de Trilha C | `docs/journey/README.md` descreve C como compilador Jack; `README.md` e `docs/track-c/README.md` usam C para Linux x86-64 | Alta | Corrigir navegação e preservar Jack como extensão distinta |
| Status da Trilha C está desatualizado | `README.md` ainda diz “Apenas C01” | Média | Atualizar com status de PRs, sem atribuir PASS pedagógico |
| Critério LEARN existe mas não foi exercido | `docs/PEDAGOGY.md` define rubrica 0–3; README informa diário não exercido | Alta | Fazer piloto com iniciantes reais, sem inventar resultados |

## Matriz de dependências conceituais

| Etapa | Conceitos exigidos | Introduzir antes de |
| --- | --- | --- |
| A01 | 0/1, função, entrada/saída, AND/NOT, tabela-verdade | Construir NAND, XOR, mutação |
| A02–A03 | composição, circuito combinacional, carry, representação binária | MUX, somador, ALU |
| A04–A06 | estado, clock, registrador, endereço, instrução | RAM, PC, CPU Hack |
| A07–A08 | ISA, assembly, assembler, tradução | Programas Hack |
| B01–B04 | CPU real vs Hack, boot, privilégio, interrupção | Kernel x86-64 |
| B05–B12 | memória física/virtual, processo, syscall, ELF, persistência | Alocador, ring 3, filesystem |
| C01–C05 | Linux CLI, processo, registradores x86-64, binário ELF, ABI | Syscalls, callbacks C/Assembly |
| C06–C12 | ponteiros, páginas, alocação, depuração | mmap, benchmarks, GDB |

A matriz é **hipótese curricular** e precisa ser validada com estudantes. Não implica que todos os capítulos já ensinem os pré-requisitos.

## Piloto observacional (a executar)

- Recrutar 2–3 participantes que declarem não ter experiência com programação ou arquitetura de computadores; consentimento e participação voluntária.
- Entregar apenas `docs/pedagogy/START-FROM-ZERO.md` e A01; não explicar as respostas durante a tarefa.
- Registrar tempo, bloqueios, pedidos de ajuda, conceitos desconhecidos e se completaram um desafio novo.
- Aplicar rubrica PACTO sem confundir acerto por cópia com compreensão.
- Repetir A01 após 7 dias sem gabarito para verificar retenção.
- Publicar somente resultados anonimizados e consentidos; não coletar dados pessoais desnecessários.

## Critérios de saída da fase piloto

- Cada aluno consegue prever os quatro casos NAND sem consultar.
- Consegue construir NOT com NAND e explicar por que funciona.
- Resolve ao menos um problema de transferência não idêntico ao exemplo.
- Explica uma limitação da analogia.
- Registra erros e correções no diário.

**Estado:** auditoria documental concluída; validação com participantes `NOT_RUN`; pontuação de eficácia pedagógica `UNVERIFIED`.
