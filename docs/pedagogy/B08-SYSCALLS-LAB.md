# B08 — Fronteira de syscalls e validação de argumentos

> Modelo executável isolado, não implementação do kernel. ENG/SCI/LEARN NOT_RUN até execução e revisão.

## Objetivo e previsão

Leia [B08 — introdução](B08-GUIDED.md). Antes de executar, descreva entradas válidas, estado inicial e resultado esperado. A analogia com um serviço de atendimento ajuda a visualizar entradas e respostas, mas **não** representa o comportamento completo de hardware, privilégios, persistência ou processos.

## Como executar

Na raiz do repositório:

```bash
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b08_syscalls.py' -v
```

Compare a previsão com cada teste. Registre commit, Python, ambiente, saída e código de retorno; não marque PASS sem observação.

## Refutação reproduzível

Remova a checagem argument>=len(memory): o teste test_out_of_bounds deixará de receber SyscallError.

Preveja o teste que falhará, faça a alteração temporária, execute e reverta. Caso a mutação sobreviva, trate como lacuna da suíte.

## Transferência

Para memória b'XYZ', preveja dispatch(1,2,...)=90 e explique por que isso não valida ponteiros virtuais reais.

## Evidência e limites

**ENG:** testes do modelo comprovados por execução. **SCI:** previsão e contraexemplo observados. **LEARN:** iniciante resolve caso inédito e explica sem analogia; NOT_RUN até avaliação real. Nenhum resultado aqui demonstra o funcionamento do kernel x86-64.
