# Checklist de revisão independente — laboratórios B05–B12

> Este documento é um roteiro de revisão. **Nenhuma revisão foi executada** por sua criação.

## Identidade da revisão

- PR e commit exato: NOT_RUN
- Revisor (distinto do autor): NOT_RUN
- Escopo e arquivos examinados: NOT_RUN
- Ambiente e comandos: NOT_RUN

## Engenharia (ENG)

- [ ] O código e o teste foram lidos separadamente?
- [ ] As entradas esperadas vêm de uma fonte independente da implementação?
- [ ] O comando de teste foi executado com exit code capturado?
- [ ] O teste falha se o comportamento esperado for deliberadamente quebrado?
- [ ] Um módulo de teste removido faz a CI falhar?
- [ ] O código alterado corresponde ao módulo e ao objetivo declarado?
- [ ] A aprovação do modelo Python não foi confundida com QEMU?

## Experimento (SCI)

- [ ] A hipótese e o critério de refutação foram escritos antes do teste?
- [ ] O controle negativo produz o resultado previsto?
- [ ] A reversão da mutação restaura o resultado positivo?
- [ ] Logs e versões são suficientes para outra pessoa reproduzir?

## Aprendizagem (LEARN)

- [ ] Há explicação de pré-requisitos e termos?
- [ ] O aluno precisa prever antes de executar?
- [ ] Há exercício de transferência sem gabarito antecipado?
- [ ] A analogia tem limites explícitos?
- [ ] O estado LEARN só muda após observação independente?

## Decisão

| Campo | Valor |
| --- | --- |
| ENG modelo | NOT_RUN |
| ENG kernel | NOT_RUN |
| SCI | NOT_RUN |
| LEARN | NOT_RUN |
| Bloqueadores | NOT_RUN |
| Correções solicitadas | NOT_RUN |
| Parecer independente | NOT_RUN |

**Não use este checklist como autorização automática de merge.** O parecer deve referenciar logs, código e commit revisados. Utilize [modelo de experimento](EXPERIMENT-RECORD-TEMPLATE.md) e [protocolo QEMU](QEMU-EVIDENCE-PROTOCOL.md).
