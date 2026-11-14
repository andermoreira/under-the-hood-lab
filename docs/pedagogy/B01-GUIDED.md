# B01 — Do executável ao boot: toolchain, linker, Limine e QEMU

> **Estado:** aula de preparação conceitual; não substitui o código nem a documentação operacional do lab. ENG/SCI/LEARN nesta alteração: NOT_RUN.

## Pré-requisitos

Antes de prosseguir, saiba distinguir bit, instrução, registrador, memória, endereço, CPU e programa; revise [a jornada A01–A08](../ROADMAP.md). Na Trilha B, a CPU é **x86-64 real/emulada**, diferente da CPU Hack da Trilha A. Se o terminal for novo, consulte a [preparação do ambiente](pedagogy/ENVIRONMENT.md) a partir da raiz `docs/`.

## 1. Problema antes da definição

Um livro precisa ser encadernado antes de ser lido; o linker organiza partes do programa em um arquivo executável.

**Previsão:** escreva como você imagina que a máquina resolve esse problema. Registre sua resposta antes de continuar.

## 2. Modelo mental

Código-fonte não é binário; compilador/assembler, linker, bootloader e emulador têm responsabilidades diferentes.

**Onde a analogia falha:** Um bootloader não é o kernel; QEMU não prova compatibilidade com hardware real.

## 3. Exemplo guiado

Desenhe o caminho fonte → objeto → ELF → bootloader → kernel e explique o papel de cada etapa.

Use um desenho ou uma tabela com colunas **evento/entrada**, **estado anterior**, **ação** e **resultado esperado**. Marque os pontos em que não conhece a resposta; consulte o glossário, não invente comportamento do hardware.

## 4. Experimento negativo

Troque hipoteticamente o endereço de entrada no linker e preveja o tipo de falha, sem executar uma imagem insegura.

Formule o resultado esperado e a observação que o refutaria. Para testes reais de kernel, use somente ambiente isolado (QEMU) e os comandos canônicos documentados no repositório; não altere a máquina host nem execute código privilegiado por suposição.

## 5. Transferência

Compare a função do linker à do assembler Hack, apontando três diferenças.

Explique a solução sem usar a analogia. Se não conseguir, registre qual pré-requisito faltou e volte à etapa correspondente.

## 6. Diário de aprendizagem

Anote hipótese inicial, previsão, comparação, erro e correção. Refaça o desafio após 1, 7 e 30 dias. **CI verde não é prova de aprendizagem**; LEARN permanece NOT_RUN até haver observação real.

**Limitações deste documento:** roteiro introdutório, não tutorial executável completo; comandos específicos, resultados reais, verificação independente e piloto com estudantes permanecem pendentes.
