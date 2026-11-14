# Backlog de validação real em QEMU — B05–B12

> **Todos os estados abaixo começam em NOT_RUN.** Nenhum experimento QEMU foi executado para elaborar este backlog.

## Por que existe esta lacuna?

A suíte Python demonstra propriedades de **modelos educacionais**, não do kernel. O próximo incremento de engenharia precisa localizar os testes canônicos existentes no repositório, verificar seus contratos e produzir logs reais.

| Prioridade | Módulo | Experimento real a localizar ou implementar | Controle negativo | Estado |
| --- | --- | --- | --- | --- |
| P0 | B05 | PMM: frames alocados e liberados no kernel | alocação duplicada ou double free | NOT_RUN |
| P0 | B06 | page fault e isolamento de página em QEMU | acesso a página não mapeada | NOT_RUN |
| P0 | B12 | boot, execução, escrita, reboot, leitura | remover uma etapa obrigatória | NOT_RUN |
| P1 | B08 | syscall do programa de usuário e retorno | ponteiro inválido | NOT_RUN |
| P1 | B09 | ELF real carregado pelo kernel | cabeçalho inválido | NOT_RUN |
| P1 | B10 | persistência de disco após reboot | escrita não persistida | NOT_RUN |
| P2 | B07 | sequência observada de tarefas reais | tarefa bloqueada escalonada | NOT_RUN |
| P2 | B11 | comando recebido via console/serial | entrada inválida | NOT_RUN |

## Critério de aceitação para cada PR de QEMU

1. Citar o arquivo e comando **existentes** do teste canônico, ou adicionar um novo com justificativa.
2. Executar o kernel real e guardar exit code, log serial, versão do QEMU e commit.
3. Provar que o teste fica vermelho com um defeito controlado.
4. Reverter o defeito e provar que volta a ficar verde.
5. Exigir parecer independente para a alegação de comportamento do kernel.
6. Atualizar ENG kernel sem modificar automaticamente SCI ou LEARN.

## Ordem de implementação sugerida

Primeiro inventariar comandos canônicos de build/boot/teste; depois implementar um único experimento vertical B05 (código do kernel → QEMU → log → assert → negativo). Reutilizar o padrão para B06 e B12. Não criar scripts que só procuram strings em arquivos-fonte como prova de execução.

## Registro por fatia

- PR/commit: NOT_RUN
- Teste QEMU real: NOT_RUN
- Log e hash do artefato: NOT_RUN
- Controle negativo: NOT_RUN
- Revisão independente: NOT_RUN
- ENG kernel: NOT_RUN

Use [protocolo de evidência](QEMU-EVIDENCE-PROTOCOL.md) e [modelo de registro](EXPERIMENT-RECORD-TEMPLATE.md).
