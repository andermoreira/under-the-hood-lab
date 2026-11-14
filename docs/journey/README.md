# Jornada guiada — do bit ao sistema operacional

> **Comece aqui.** Não comece pelo catálogo de referência nem pelo código do kernel.

## Primeiro contato (15 minutos)
1. Se nunca programou, comece por [Primeira experiência sem programação](../pedagogy/START-FROM-ZERO.md) e [Preparação do ambiente](../pedagogy/ENVIRONMENT.md).\n2. Leia [Guia do iniciante](../INICIANTE.md).
2. Leia a [aula NAND](../LESSON_A01_NAND.md) e registre sua previsão ANTES de executar.
4. Rode `make test` para validar o modelo de referência Python.
5. Compare o resultado observado com a hipótese.
6. Consulte o [glossário](../GLOSSARIO.md) apenas quando necessário.

## A trilha principal
- **Parte A (A01–A08):** NAND, circuitos, ALU, memória, CPU Hack, assembler e programas.
- **Ponte:** do circuito ao executável: representação binária, ABI, linker e ELF.
- **Parte B (B01–B12):** boot x86-64, kernel, interrupções, memória, scheduler, modo usuário, arquivos e shell.
- **Capstone:** inicializar, executar dois programas isolados, persistir arquivo, reiniciar e comprovar recuperação.

## Trilha C opcional
VM translator, linguagem Jack, compilador e SO Hack, seguindo os projetos 7–12 do Nand2Tetris. Não é pré-requisito para B01.

## Ritmo de cada módulo
Fenômeno → hipótese escrita → implementação → teste positivo/limite/negativo → inspeção → explicação sem analogia → desafio de transferência → revisão após 1, 7 e 30 dias.

## Três aprovações independentes
1. **ENG:** software atende ao contrato (testes executados).
2. **SCI:** experimento demonstra a hipótese e registra contraexemplo/limites.
3. **LEARN:** estudante explica, prediz e transfere sem consultar a resposta.

Uma aprovação não substitui outra. `NOT_RUN` não é `PASS`.

## Próximos passos
- [Workbook A01](../workbooks/A01.md)
- [Auditoria pedagógica](../PEDAGOGICAL-AUDIT.md)\n- [Auditoria da jornada de iniciantes](../pedagogy/BEGINNER-AUDIT.md)
- [Referências](../REFERENCES.md)
