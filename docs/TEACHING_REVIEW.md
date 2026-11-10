# Revisão pedagógica independente — rubrica

**Público-alvo:** conhece variáveis, funções, condicionais e loops; não conhece eletrônica, arquitetura ou sistemas operacionais.

## Checklist de conteúdo (avaliar por capítulo)
- [ ] A aula começa com um problema concreto e declara pré-requisitos verificáveis?
- [ ] Cada termo técnico aparece definido antes de ser exigido?
- [ ] Existe uma analogia real, um mapeamento explícito e a seção onde ela falha?
- [ ] O Mermaid é legível, representa o mecanismo correto e renderiza no GitHub?
- [ ] Existem ao menos dois exemplos resolvidos, incluindo um caso-limite?
- [ ] O estudante faz previsão **antes** de executar?
- [ ] Os comandos são reproduzíveis com dependências e resultados esperados claros?
- [ ] Há controle negativo, caso inválido e explicação do que a falha demonstra?
- [ ] O estudante explica o mecanismo sem a analogia?
- [ ] Há exercícios de recuperação, aplicação e transferência, com gabarito útil?
- [ ] A revisão espaçada em 1, 7 e 30 dias tem atividade de recuperação, não só releitura?
- [ ] ENG e LEARN são avaliados separadamente, com commit e evidência?

## Protocolo de revisão com estudante iniciante
1. Entregar o capítulo **sem** apresentar o gabarito.
2. Pedir que o leitor sublinhe termos desconhecidos e momentos em que precisou consultar fonte externa.
3. Registrar tempo, previsões, erros, perguntas e execução de comandos.
4. Pedir explicação do mecanismo sem analogias e resolução de exercício novo.
5. Avaliar 0–3 nas dimensões prever, construir, explicar, refutar e transferir, conforme [PACTO](PEDAGOGY.md).
6. Classificar cada problema como bloqueante, relevante ou editorial; abrir issue com capítulo, trecho e reprodução.
7. Revalidar com outra pessoa ou uma segunda tentativa após correção.

## Estados
- **PASS:** evidência executada e revisão independente demonstram o critério.
- **FAIL:** evidência concreta de erro, confusão bloqueante ou gate quebrado.
- **NOT_RUN:** verificação ainda não realizada.
- **UNVERIFIED:** relato ou evidência incompleta, sem reprodução.

**Não confundir:** o teste `tests/test_pedagogical_coverage.py` só verifica estrutura. Não avalia precisão técnica, compreensão humana ou Mermaid renderizado.

## Registro de revisão (copiar por capítulo)
| Campo | Valor |
|---|---|
| Capítulo / commit | |
| Revisor e perfil | |
| Ambiente e comandos | |
| Mermaid renderizado? | NOT_RUN |
| Exemplos executados? | NOT_RUN |
| Explicação independente? | NOT_RUN |
| Exercício de transferência? | NOT_RUN |
| Erros e correções | |
| ENG / LEARN | NOT_RUN / NOT_RUN |
| Decisão | NÃO APROVAR sem evidência |
