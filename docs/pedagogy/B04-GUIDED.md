# B04 — Timer e teclado: eventos externos

> **Estado:** aula de preparação conceitual; não substitui o código nem a documentação operacional do lab. ENG/SCI/LEARN nesta alteração: NOT_RUN.

## Pré-requisitos

Antes de prosseguir, saiba distinguir bit, instrução, registrador, memória, endereço, CPU e programa; revise [a jornada A01–A08](../ROADMAP.md). Na Trilha B, a CPU é **x86-64 real/emulada**, diferente da CPU Hack da Trilha A. Se o terminal for novo, consulte a [preparação do ambiente](pedagogy/ENVIRONMENT.md) a partir da raiz `docs/`.

## 1. Problema antes da definição

Um relógio desperta uma pessoa para executar uma tarefa periódica; um botão anuncia uma ação do usuário.

**Previsão:** escreva como você imagina que a máquina resolve esse problema. Registre sua resposta antes de continuar.

## 2. Modelo mental

Interrupções externas permitem reagir a timer e teclado sem consulta contínua no modelo simplificado.

**Onde a analogia falha:** Relógio humano não representa IRQ, controladores, acknowledge, perda de eventos ou latência.

## 3. Exemplo guiado

Trace três ticks de timer e dois eventos de teclado, separando ordem de chegada e tratamento.

Use um desenho ou uma tabela com colunas **evento/entrada**, **estado anterior**, **ação** e **resultado esperado**. Marque os pontos em que não conhece a resposta; consulte o glossário, não invente comportamento do hardware.

## 4. Experimento negativo

Imagine ausência de acknowledge do controlador; formule hipótese sobre interrupções repetidas ou bloqueadas conforme hardware.

Formule o resultado esperado e a observação que o refutaria. Para testes reais de kernel, use somente ambiente isolado (QEMU) e os comandos canônicos documentados no repositório; não altere a máquina host nem execute código privilegiado por suposição.

## 5. Transferência

Projete uma fila de eventos com capacidade limitada e explique como detectar perda.

Explique a solução sem usar a analogia. Se não conseguir, registre qual pré-requisito faltou e volte à etapa correspondente.

## 6. Diário de aprendizagem

Anote hipótese inicial, previsão, comparação, erro e correção. Refaça o desafio após 1, 7 e 30 dias. **CI verde não é prova de aprendizagem**; LEARN permanece NOT_RUN até haver observação real.

**Limitações deste documento:** roteiro introdutório, não tutorial executável completo; comandos específicos, resultados reais, verificação independente e piloto com estudantes permanecem pendentes.
