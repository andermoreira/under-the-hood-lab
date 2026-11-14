# Avaliação com iniciantes — protocolo de aprendizagem B05–B12

> **LEARN NOT_RUN.** Nenhuma observação com estudantes foi realizada ou inferida nesta PR.

## Pergunta da avaliação

Uma pessoa sem conhecimento prévio de sistemas operacionais consegue **prever, executar, explicar e transferir** os conceitos após usar as aulas?

## Recrutamento e ética

Convide participantes voluntários que não tenham estudado MMU, escalonadores, ELF ou syscalls. Informe que a avaliação é do material, não da pessoa. Evite coletar nomes, emails, gravações ou dados sensíveis. Permita desistência a qualquer momento.

## Roteiro de sessão (45–60 minutos)

1. **Pré-teste (5 min):** peça que expliquem, em palavras próprias, o que é um endereço de memória, um processo e um arquivo. Marque lacunas, sem corrigir.
2. **Estudo (15 min):** escolha **um** laboratório de B05–B12. Observe se o estudante consegue localizar pré-requisitos, exemplos e comandos sem ajuda.
3. **Previsão (5 min):** antes da execução, registre a saída esperada e o motivo.
4. **Experimento (10 min):** peça que rode o teste positivo e a mutação negativa; observe se interpreta uma falha.
5. **Transferência (10 min):** dê um caso novo não mostrado na aula; peça explicação sem consultar o gabarito.
6. **Retenção (após 7 dias, opcional):** repita uma tarefa equivalente, não idêntica.

## Rubrica operacional

| Critério | 0 — Não demonstrou | 1 — Com ajuda | 2 — Independente |
| --- | --- | --- | --- |
| Conceito | Não distingue termos | Explica parcialmente | Explica com precisão e limites |
| Previsão | Não propõe hipótese | Hipótese sem justificativa | Prevê e justifica |
| Execução | Não executa | Executa guiado | Executa e interpreta |
| Refutação | Confunde falha com sucesso | Identifica falha | Explica causa e reversão |
| Transferência | Não resolve caso novo | Resolve com dicas | Resolve e generaliza |

**Não reduza a avaliação a um número isolado.** Registre também o tipo de dúvida, o trecho que causou dificuldade, tempo aproximado e intervenção do facilitador. Uma nota alta em execução guiada não equivale a aprendizagem independente.

## Critério de revisão pedagógica

Se o estudante precisar de ajuda para interpretar um termo, comando ou saída, abra uma issue citando apenas o módulo, o obstáculo observado e a melhoria proposta. Corrija o material e repita a avaliação com novo participante. Não transforme o feedback de uma única pessoa em generalização.

## Registro inicial

| Campo | Estado |
| --- | --- |
| Módulo/commit | NOT_RUN |
| Pré-requisitos do participante | NOT_RUN |
| Previsão e justificativa | NOT_RUN |
| Comando/resultado | NOT_RUN |
| Mutação e explicação | NOT_RUN |
| Caso de transferência | NOT_RUN |
| Rubrica e obstáculos | NOT_RUN |
| Avaliação independente | NOT_RUN |
| LEARN | NOT_RUN |

## Separação de evidências

A CI pode validar **ENG** dos modelos. O experimento negativo documentado pode apoiar **SCI**. Apenas observações humanas estruturadas podem apoiar **LEARN**. Não marque LEARN PASS com base em quantidade de páginas, testes ou PRs.
