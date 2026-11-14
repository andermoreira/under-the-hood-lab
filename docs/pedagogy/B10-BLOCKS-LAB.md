# B10 — Armazenamento em blocos: laboratório verificável

> Modelo didático, não código do kernel. ENG/SCI/LEARN NOT_RUN até execução e avaliação independente.

## Pré-requisitos e previsão

Consulte [a jornada](../journey/README.md) e o roteiro [B10](B10-GUIDED.md). **Antes de executar:** Dez bytes com blocos de quatro: preveja 4+4+2, três blocos. Explique por que esse experimento não prova persistência após reboot.

## Execução reproduzível

Na raiz do repositório:

```bash
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b10_blocks.py' -v
```

Leia o código em `docs/pedagogy/examples/b10_blocks.py` e registre cada estado esperado. O teste é do modelo, **não** do kernel.

## Experimento negativo

Troque range(0,len(data),block_size) por range(0,len(data)-1,block_size): test_ten_bytes falhará para alguns comprimentos; acrescente um teste de byte único.

Registre hipótese, saída e causa; restaure o código original e execute novamente. Se a mutação não falhar como previsto, registre a lacuna e melhore o teste em vez de declarar PASS.

## Transferência e limitações

Crie um caso novo não presente nos testes, resolva no papel e explique a solução sem analogia. Compare a simplificação do modelo com o componente real da Trilha B: quais propriedades faltam (concorrência, hardware, isolamento ou persistência)?

**ENG:** só após execução com commit e saída; **SCI:** após hipótese e refutação observadas; **LEARN:** somente com iniciante demonstrando compreensão. Revisão espaçada em 1, 7 e 30 dias.
