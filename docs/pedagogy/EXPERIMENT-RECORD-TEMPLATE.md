# Registro de experimento reproduzível

Copie este modelo para cada experimento. **Não marque PASS sem executar.** Comece todos os estados em NOT_RUN.

## Identificação

- ID do experimento: NOT_RUN
- Módulo B05–B12: NOT_RUN
- Objetivo e hipótese falsificável: NOT_RUN
- Commit completo / branch: NOT_RUN
- Revisor independente: NOT_RUN

## Ambiente

| Campo | Valor |
| --- | --- |
| Sistema operacional | NOT_RUN |
| Versão Python | NOT_RUN |
| Versão QEMU (se aplicável) | NOT_RUN |
| Compilador / toolchain | NOT_RUN |
| Configuração e flags | NOT_RUN |
| Hash da imagem/artefato | NOT_RUN |

## Critério de aprovação **antes** da execução

- Comando positivo exato: NOT_RUN
- Saída/exit code esperados: NOT_RUN
- Mutação negativa escolhida: NOT_RUN
- Sintoma esperado da mutação: NOT_RUN
- Como restaurar o baseline: NOT_RUN

## Observações

| Execução | Comando | Exit code | Log/artefato | Estado |
| --- | --- | --- | --- | --- |
| Baseline positivo | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| Controle negativo | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| Baseline restaurado | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |

## Interpretação

- Hipótese confirmada ou refutada? NOT_RUN
- Resultado inesperado e investigação: NOT_RUN
- Limites do experimento: NOT_RUN
- Evidência contraditória: NOT_RUN
- Revisão independente e parecer: NOT_RUN

## Estados separados

| Dimensão | Estado inicial | Evidência necessária |
| --- | --- | --- |
| ENG modelo | NOT_RUN | testes Python, logs e código de saída |
| ENG kernel | NOT_RUN | QEMU, serial, build e logs reais |
| SCI | NOT_RUN | previsão + controle negativo observado |
| LEARN | NOT_RUN | avaliação estruturada de iniciante |

**Estados permitidos:** PASS, FAIL, NOT_RUN, UNVERIFIED. Um resultado de uma dimensão não autoriza automaticamente PASS nas demais. Use [protocolo QEMU](QEMU-EVIDENCE-PROTOCOL.md) e [avaliação pedagógica](BEGINNER-ASSESSMENT.md).
