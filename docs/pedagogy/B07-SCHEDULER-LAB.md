# B07 — Scheduler round-robin: laboratório verificável

> Modelo didático, não código do kernel. ENG/SCI/LEARN NOT_RUN até execução e avaliação independente.

## Pré-requisitos e previsão

Consulte [a jornada](../journey/README.md) e o roteiro [B07](B07-GUIDED.md). **Antes de executar:** A,B,C prontos; sete ticks de quantum unitário. Preveja A B C A B C A. Se B bloquear antes da execução, preveja A C A C.

## Execução reproduzível

Na raiz do repositório:

```bash
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b07_scheduler.py' -v
```

Leia o código em `docs/pedagogy/examples/b07_scheduler.py` e registre cada estado esperado. O teste é do modelo, **não** do kernel.

## Experimento negativo

Remova queue.append(task): test_rotation deve falhar.

Registre hipótese, saída e causa; restaure o código original e execute novamente. Se a mutação não falhar como previsto, registre a lacuna e melhore o teste em vez de declarar PASS.

## Transferência e limitações

Crie um caso novo não presente nos testes, resolva no papel e explique a solução sem analogia. Compare a simplificação do modelo com o componente real da Trilha B: quais propriedades faltam (concorrência, hardware, isolamento ou persistência)?

**ENG:** só após execução com commit e saída; **SCI:** após hipótese e refutação observadas; **LEARN:** somente com iniciante demonstrando compreensão. Revisão espaçada em 1, 7 e 30 dias.
