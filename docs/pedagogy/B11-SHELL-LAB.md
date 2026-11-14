# B11 — Parser de comandos e erros de entrada

> Modelo executável isolado, não implementação do kernel. ENG/SCI/LEARN NOT_RUN até execução e revisão.

## Objetivo e previsão

Leia [B11 — introdução](B11-GUIDED.md). Antes de executar, descreva entradas válidas, estado inicial e resultado esperado. A analogia com um serviço de atendimento ajuda a visualizar entradas e respostas, mas **não** representa o comportamento completo de hardware, privilégios, persistência ou processos.

## Como executar

Na raiz do repositório:

```bash
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b11_shell.py' -v
```

Compare a previsão com cada teste. Registre commit, Python, ambiente, saída e código de retorno; não marque PASS sem observação.

## Refutação reproduzível

Substitua line.split() por line.split(' '): test_whitespace e test_empty devem revelar a diferença.

Preveja o teste que falhará, faça a alteração temporária, execute e reverta. Caso a mutação sobreviva, trate como lacuna da suíte.

## Transferência

Explique por que split() não implementa quoting, pipes ou redirecionamento; proponha um teste que exigiria parser mais completo.

## Evidência e limites

**ENG:** testes do modelo comprovados por execução. **SCI:** previsão e contraexemplo observados. **LEARN:** iniciante resolve caso inédito e explica sem analogia; NOT_RUN até avaliação real. Nenhum resultado aqui demonstra o funcionamento do kernel x86-64.
