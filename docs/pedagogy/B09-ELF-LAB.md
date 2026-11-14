# B09 — Validador mínimo de cabeçalho ELF: laboratório verificável

> Modelo didático, não código do kernel. ENG/SCI/LEARN NOT_RUN até execução e avaliação independente.

## Pré-requisitos e previsão

Consulte [a jornada](../journey/README.md) e o roteiro [B09](B09-GUIDED.md). **Antes de executar:** Explique por que 0x7f ELF é uma assinatura e por que uma assinatura válida não comprova que o arquivo é seguro para carregar.

## Execução reproduzível

Na raiz do repositório:

```bash
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b09_elf.py' -v
```

Leia o código em `docs/pedagogy/examples/b09_elf.py` e registre cada estado esperado. O teste é do modelo, **não** do kernel.

## Experimento negativo

Troque a comparação data[4]!=2 por data[4]!=1: test_valid_ident e test_elf32 devem falhar.

Registre hipótese, saída e causa; restaure o código original e execute novamente. Se a mutação não falhar como previsto, registre a lacuna e melhore o teste em vez de declarar PASS.

## Transferência e limitações

Crie um caso novo não presente nos testes, resolva no papel e explique a solução sem analogia. Compare a simplificação do modelo com o componente real da Trilha B: quais propriedades faltam (concorrência, hardware, isolamento ou persistência)?

**ENG:** só após execução com commit e saída; **SCI:** após hipótese e refutação observadas; **LEARN:** somente com iniciante demonstrando compreensão. Revisão espaçada em 1, 7 e 30 dias.
