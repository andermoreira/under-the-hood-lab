# B05 — Alocador first-fit: laboratório verificável

> Modelo didático, não código do kernel. ENG/SCI/LEARN NOT_RUN até execução e avaliação independente.

## Pré-requisitos e previsão

Consulte [a jornada](../journey/README.md) e o roteiro [B05](B05-GUIDED.md). **Antes de executar:** Frames livres 2, 5, 7: preveja os dois primeiros retornos; depois esgote o conjunto. Explique por que uma região reservada nunca deve entrar na lista de livres.

## Execução reproduzível

Na raiz do repositório:

```bash
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b05_frames.py' -v
```

Leia o código em `docs/pedagogy/examples/b05_frames.py` e registre cada estado esperado. O teste é do modelo, **não** do kernel.

## Experimento negativo

Troque min(self.free) por max(self.free): test_first_fit deve falhar.

Registre hipótese, saída e causa; restaure o código original e execute novamente. Se a mutação não falhar como previsto, registre a lacuna e melhore o teste em vez de declarar PASS.

## Transferência e limitações

Crie um caso novo não presente nos testes, resolva no papel e explique a solução sem analogia. Compare a simplificação do modelo com o componente real da Trilha B: quais propriedades faltam (concorrência, hardware, isolamento ou persistência)?

**ENG:** só após execução com commit e saída; **SCI:** após hipótese e refutação observadas; **LEARN:** somente com iniciante demonstrando compreensão. Revisão espaçada em 1, 7 e 30 dias.
