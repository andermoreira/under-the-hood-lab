# Jornada guiada — do bit ao sistema operacional

> **Comece aqui.** Não comece pelo catálogo de referência nem pelo código do kernel.

## Primeiro contato

1. Se nunca programou, comece por [Primeira experiência sem programação](../pedagogy/START-FROM-ZERO.md).
2. Consulte a [Preparação do ambiente](../pedagogy/ENVIRONMENT.md) antes de usar terminal.
3. Leia o [Guia do iniciante](../INICIANTE.md).
4. Estude a [aula NAND](../LESSON_A01_NAND.md) e registre sua previsão **antes** de executar.
5. Quando o ambiente estiver preparado, rode `make test` para verificar o modelo de referência.
6. Compare o observado com a hipótese; consulte o [glossário](../GLOSSARIO.md) quando necessário.

## A trilha principal

- **Trilha A (A01–A08):** NAND, circuitos, ALU, memória, CPU Hack, assembler e programas. Veja [workbook A01](../workbooks/A01.md) e [progressão A02–A08](../pedagogy/A02-A08-LEARNING-PATH.md).
- **Ponte:** da CPU didática Hack à arquitetura x86-64, representação binária, ABI, linker e ELF. **A CPU Hack não executa binários x86-64.**
- **Trilha B (B01–B12):** boot x86-64, kernel, interrupções, memória, scheduler, modo usuário, arquivos e shell.
- **Trilha C (C01–C12, opcional):** programação low-level em Linux x86-64; veja [roteiro real da Trilha C](../track-c/README.md). O kernel da Trilha B não implementa automaticamente a ABI Linux.
- **Extensão opcional Nand2Tetris:** VM translator, Jack, compilador e SO Hack (projetos 7–12). Esta extensão **não é a Trilha C** deste repositório.

## Ritmo de cada módulo

Fenômeno → hipótese escrita → implementação → teste positivo/limite/negativo → inspeção → explicação sem analogia → desafio de transferência → revisão após 1, 7 e 30 dias.

## Três aprovações independentes

1. **ENG:** software atende ao contrato (testes executados).
2. **SCI:** experimento demonstra a hipótese e registra contraexemplo/limites.
3. **LEARN:** estudante explica, prediz e transfere sem consultar a resposta.

Uma aprovação não substitui outra. `NOT_RUN` não é `PASS`.

## Próximos passos

- [Workbook A01](../workbooks/A01.md)
- [Auditoria pedagógica](../PEDAGOGICAL-AUDIT.md)
- [Auditoria da jornada de iniciantes](../pedagogy/BEGINNER-AUDIT.md)
- [Referências](../REFERENCES.md)
