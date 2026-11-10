# F05 — De código-fonte a instruções de máquina

**Público:** sabe programar, não conhece eletrônica. **Pré-requisito:** [F04-ESTADO-CPU ](F04-ESTADO-CPU.md). **Tempo sugerido:** 60–100 minutos.

## 1. Problema concreto
O processador não executa diretamente palavras como `while` ou `print`. Ele executa instruções codificadas como bits, segundo um conjunto de instruções (ISA). Assembly é uma representação textual próxima dessas instruções; um assembler transforma símbolos e mnemônicos em código de máquina.

## 2. Conceitos construídos passo a passo
No computador Hack, `@21` é uma instrução A que carrega o valor 21 no registrador A. A codificação usa 16 bits: o primeiro bit é 0 e os outros 15 representam 21. Assim, `@21` vira `0000000000010101`. Isso é específico da ISA Hack, não de x86-64.

## Analogia com o mundo real
Assembly se parece com uma lista de instruções curtas para uma máquina especializada; o assembler é um tradutor que converte essas instruções para códigos que a máquina reconhece. O linker organiza partes produzidas separadamente, como a montagem de um manual com referências cruzadas.

### Onde a analogia deixa de funcionar
Tradução não implica que todas as arquiteturas entendam as mesmas instruções. Assembly não é uma linguagem universal e um linker não garante que o programa funcione quando executado.

## 3. Exemplo resolvido
Um programa fonte pode passar por compilação, montagem (assembly) e ligação (linkedição). O linker resolve símbolos e organiza seções em um executável. No kernel, o carregador e o formato ELF também importam; `main` e `printf` não surgem automaticamente.

## 4. Segundo exemplo e caso-limite
Exemplo resolvido: `@0` produz dezesseis zeros; `@32767` produz 0 seguido de quinze bits 1. `@32768` não cabe no campo de 15 bits da instrução A. Essa é uma restrição da ISA, não da capacidade de um inteiro Python.

## 5. Experimento guiado e leitura do projeto
Abra `tools/hack_assembler.py`, localize a validação de instruções A e compare `assemble('@21\n')` com o valor esperado. Execute `python3 -m unittest tests/test_a07_assembler.py` se o ambiente e o módulo estiverem disponíveis; registre o resultado real.

**Antes de executar:** escreva uma previsão específica. **Depois:** registre comando, saída observada, exit code, commit e explicação para qualquer divergência. Nenhum resultado de execução foi verificado nesta revisão editorial.

## 6. Onde o modelo simplifica
Os exemplos são modelos didáticos. Não extrapole automaticamente de Python para comportamento físico, de Hack para x86-64 ou de uma demonstração para segurança de produção. Identifique o que foi observado e o que permanece hipótese.

## 7. Exercícios progressivos
**Recuperação e aplicação:** Defina ISA, assembly, assembler, linker e executável; explique por que duas CPUs diferentes podem usar instruções distintas.

**Transferência:** Explique por que um binário Hack não pode ser executado diretamente como código x86-64 e o que um emulador precisaria fazer.

<details>
<summary>Orientações de correção — abra depois de tentar</summary>

Uma resposta satisfatória define os termos com precisão, apresenta pelo menos um exemplo numérico ou operacional, explicita o caso-limite e distingue a evidência executada de uma previsão. Compare sua solução com as definições e exemplos deste capítulo; se houver dúvida, registre a lacuna e busque revisão independente.
</details>

## 8. Evidência e revisão espaçada
**ENG: NOT_RUN** — não há execução de comandos nesta alteração. **LEARN: NOT_RUN** — o estudante ainda não demonstrou entendimento. Revisar sem consulta após **1 dia**, **7 dias** e **30 dias**. Registrar erro inicial, correção e nova tentativa.

[Índice da Trilha 0](../FOUNDATIONS.md)
