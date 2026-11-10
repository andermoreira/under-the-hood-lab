# Trilha 0 — Fundamentos para quem sabe programar

**Público:** conhece variáveis, funções, condicionais e loops; não precisa conhecer eletrônica, hardware, assembly ou sistemas operacionais.

## Contrato de ensino
- Todo termo técnico novo é definido antes de ser exigido.
- Toda aula inclui fenômeno observável, explicação progressiva, exemplo resolvido, experimento reproduzível, erros comuns, exercícios graduados e evidências.
- O código real só entra depois de um modelo mental verificável.
- **ENG** comprova comportamento do software; **LEARN** requer explicação própria e transferência. Um não implica o outro.
- Sem exigir equipamentos eletrônicos. Portas são modelos lógicos, não promessas sobre tensão e temporização.
- A trilha A ensina a construção de um computador Hack; a trilha B explora um kernel x86-64. São arquiteturas diferentes.

## Percurso e dependências
| Unidade | Pergunta | Pré-requisito | Próximo passo |
|---|---|---|---|
| F01 | Como representar informação? | Programação básica | F02 |
| F02 | Como calcular com bits? | F01 | A01 |
| F03 | O que uma porta lógica faz? | F02 | A01 |
| F04 | Como guardar estado e executar instruções? | F03 | A02–A05 |
| F05 | Como texto vira instrução de máquina? | F04 | A06–A08, B01 |
| F06 | O que são endereços, ponteiros e páginas? | F01, F04 | B05–B06 |
| F07 | Como o computador começa a executar um kernel? | F04, F05 | B01–B04 |
| F08 | O que um sistema operacional protege e fornece? | F06, F07 | B07–B12 |

Comece por [F01](foundations/F01-BITS-BYTES.md), depois [F02](foundations/F02-LOGICA.md) e [A01](workbooks/A01.md). Os demais F03–F08 são **planejados, NOT_RUN**: a tabela não significa que já existam aulas completas.

## Modelo de capítulo
1. Objetivo observável e conhecimento prévio.
2. Problema concreto, sem jargão.
3. Conceitos novos definidos e desenvolvidos em passos pequenos.
4. Diagramas ou tabelas com limites explícitos.
5. Dois exemplos resolvidos, incluindo caso-limite.
6. Experimento seguro com instruções, previsão e interpretação.
7. Leitura comentada do código do repositório.
8. Erros comuns, contraexemplos e testes negativos.
9. Exercícios de recuperação, aplicação e transferência.
10. Gabarito comentado separado e revisão em 1, 7 e 30 dias.
11. Evidências ENG/LEARN e limites do que foi comprovado.

**Política de revisão:** não medir qualidade por contagem de palavras ou presença de títulos. Revisão humana independente deve tentar a aula sem conhecimento prévio de hardware, registrar pontos de confusão e pedir explicação sem analogias.
