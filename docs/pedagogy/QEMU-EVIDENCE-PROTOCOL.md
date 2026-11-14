# Protocolo de evidência — modelo Python versus kernel QEMU

> **Estado inicial: NOT_RUN.** Este protocolo é uma especificação de validação, não relatório de execução.

## Por que dois tipos de teste?

O modelo Python ajuda a entender uma regra isolada. O kernel x86-64 tem contratos adicionais: estado de CPU, MMU, dispositivos, falhas de hardware e persistência. **Um teste do modelo não comprova o comportamento do kernel.**

## Matriz de comparação

| Módulo | Modelo Python | Evidência desejada do kernel | Contraexemplo mínimo |
| --- | --- | --- | --- |
| B05 | alocar, esgotar, liberar | log serial de PMM e contagem exata de frames | double free rejeitado |
| B06 | offset e permissão | QEMU mapeia/desmapeia página, sem vazamento | página ausente provoca #PF esperado |
| B07 | ordem round-robin | trace serial de tarefas do kernel | troca incorreta detectada |
| B08 | despacho de syscall | retorno real de ring 3 ao kernel | ponteiro inválido contido |
| B09 | assinatura ELF | loader executa programa ELF de teste | ELF inválido recusado |
| B10 | divisão em blocos | escrever, reiniciar VM e ler disco | leitura inconsistente detectada |
| B11 | parser simples | shell do kernel recebe e responde comando | comando inválido não derruba VM |
| B12 | checklist booleano | sequência completa boot → programa → disco → reboot → leitura | falha isolada produz gate vermelho |

A matriz descreve **evidência a coletar**. Não afirma que os testes correspondentes foram executados nesta PR.

## Procedimento de execução

1. Fixe o commit e anote host, compilador, QEMU, flags, imagem de disco e seed.
2. Rode os comandos canônicos de build/teste documentados no repositório. Não invente marcadores seriais: leia os testes existentes e confirme a string esperada.
3. Capture comando, código de saída, stdout/stderr, logs seriais e hash do artefato.
4. Rode um **controle negativo** que compile mas quebre uma propriedade do módulo; confirme que o gate detecta a falha.
5. Restaure a alteração, rode o controle positivo novamente e compare as saídas.
6. Peça revisão independente dos logs e da correspondência entre teste e requisito.

## Estados de evidência

- **PASS:** comando executado, resultado observado e critério satisfeito.
- **FAIL:** execução observada contradiz critério.
- **NOT_RUN:** execução ainda não realizada.
- **UNVERIFIED:** alegação sem artefato auditável ou observação insuficiente.

Separe **ENG modelo**, **ENG kernel**, **SCI** (hipótese + refutação) e **LEARN** (avaliação com iniciante). Nenhuma dessas dimensões deve herdar PASS automaticamente da outra.

## Registro por execução

| Campo | Preencher |
| --- | --- |
| Commit e branch | NOT_RUN |
| Requisito e critério | NOT_RUN |
| Ambiente/versões | NOT_RUN |
| Comando exato | NOT_RUN |
| Exit code e log serial | NOT_RUN |
| Artefato/hash | NOT_RUN |
| Mutação negativa e reversão | NOT_RUN |
| Revisão independente | NOT_RUN |
| ENG modelo / ENG kernel / SCI / LEARN | NOT_RUN / NOT_RUN / NOT_RUN / NOT_RUN |

## Prioridade de implementação

Comece pelos módulos com testes reais já existentes no repositório; compare o contrato atual com a matriz antes de alterar scripts. Evite gates de simples presença de arquivo ou de string que possam ser satisfeitos sem executar o kernel.
