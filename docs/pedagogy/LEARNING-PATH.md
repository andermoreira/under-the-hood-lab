# Trilha de aprendizagem — modelos B05–B12

> Guia de estudo para autodidatas. **LEARN NOT_RUN:** este roteiro ainda não foi avaliado com estudantes.

## Como estudar

Cada módulo tem cinco passos: (1) conceito, (2) previsão escrita, (3) experimento, (4) controle negativo e (5) transferência para um caso novo. Não confunda o modelo Python com o kernel executado no QEMU.

| Ordem | Módulo | Pergunta central | Pré-requisito | Critério de transferência |
| --- | --- | --- | --- | --- |
| 1 | [B05 Frames](B05-FRAMES-LAB.md) | Quem possui cada frame? | inteiros, conjuntos | explicar double-free |
| 2 | [B06 Paging](B06-PAGING-LAB.md) | Como endereço virtual vira físico? | B05, divisão e resto | calcular tradução inédita |
| 3 | [B07 Scheduler](B07-SCHEDULER-LAB.md) | Quem recebe CPU a seguir? | filas, B05 | prever trace com bloqueio |
| 4 | [B08 Syscalls](B08-SYSCALLS-LAB.md) | Por que validar entrada do usuário? | B06, funções | detectar ponteiro inválido |
| 5 | [B09 ELF](B09-ELF-LAB.md) | Como reconhecer um executável? | bytes, B08 | rejeitar cabeçalho truncado |
| 6 | [B10 Blocos](B10-BLOCKS-LAB.md) | Como dividir dados em blocos? | bytes, divisão inteira | calcular blocos sem rodar |
| 7 | [B11 Shell](B11-SHELL-LAB.md) | Como interpretar um comando? | strings, listas | rejeitar entrada ambígua |
| 8 | [B12 Capstone](B12-CAPSTONE-LAB.md) | Que evidência prova integração? | B05–B11 | identificar prova ausente |

## Primeira sessão recomendada

Comece pelo roteiro [Primeira sessão](FIRST-SESSION.md), que apresenta previsão, alocação de frames, exaustão, mutação negativa e solução comentada. Se encontrar erro de ambiente, consulte [Solução de problemas](TROUBLESHOOTING.md).

## Rotina de estudo para cada módulo

1. Explique o conceito sem consultar o material.
2. Faça uma previsão sobre um caso que ainda não executou.
3. Execute `python3 docs/pedagogy/run_model_tests.py` e anote versão, commit, saída e exit code.
4. Introduza uma mutação negativa **em cópia local**, confira que um teste detecta o defeito e restaure.
5. Resolva um problema novo e descreva os limites do modelo.

## Critério para avançar

Você deve conseguir explicar a hipótese, interpretar um teste vermelho e resolver um caso diferente do exemplo. Se apenas reproduziu comandos, volte ao exercício de transferência. Isso é **orientação de estudo**, não medição de aprendizagem.

## Próxima etapa: hardware real

Após os modelos, consulte [protocolo QEMU](QEMU-EVIDENCE-PROTOCOL.md). Evidências ENG do kernel exigem execução real e logs. Resultados SCI exigem hipóteses e controles. LEARN exige avaliação independente com iniciantes: [protocolo](BEGINNER-ASSESSMENT.md).
