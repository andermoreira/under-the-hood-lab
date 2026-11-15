# Protocolo de sessão LEARN — execução pelo estudante

> Estado inicial de qualquer sessão: **NOT_RUN**. Este documento não certifica aprendizagem.

## Antes de executar (sem consultar a solução)

1. Escolha um único módulo e registre commit, sistema, versão das ferramentas e duração planejada.
2. No diário correspondente, escreva hipótese própria, resultado previsto e explicação causal.
3. Registre uma situação que deveria falhar e por quê.

## Durante a execução

1. Rode o gate canônico e salve comando, saída e exit code.
2. Execute o controle negativo em ambiente isolado, sem alterar a branch principal.
3. Reexecute o caso positivo após reverter a mutação.
4. Separe observações reais de interpretações e de lacunas.

## Depois

1. Compare a hipótese original com o resultado, sem editar retroativamente a hipótese.
2. Preencha a rubrica 0–3 do diário; não delegue essa avaliação à IA.
3. Registre um problema novo resolvido sem copiar a solução.
4. Programe revisões de 1, 7 e 30 dias; datas agendadas não equivalem a revisões concluídas.
5. Peça revisão independente com referência a evidências e commit.

## Checklist de saída

- [ ] Previsão anterior ao teste
- [ ] Comandos, versões e commit reproduzíveis
- [ ] Evidência positiva e controle negativo
- [ ] Explicação da diferença entre esperado e observado
- [ ] Rubrica preenchida pelo estudante
- [ ] Revisões 1/7/30 realizadas, não apenas agendadas
- [ ] Revisão independente registrada

Nenhuma caixa deve ser marcada automaticamente por testes de CI ou por IA.
