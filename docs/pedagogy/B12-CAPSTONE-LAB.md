# B12 — Contrato de integração e evidência de recuperação

> Modelo executável isolado, não implementação do kernel. ENG/SCI/LEARN NOT_RUN até execução e revisão.

## Objetivo e previsão

Leia [B12 — introdução](B12-GUIDED.md). Antes de executar, descreva entradas válidas, estado inicial e resultado esperado. A analogia com um serviço de atendimento ajuda a visualizar entradas e respostas, mas **não** representa o comportamento completo de hardware, privilégios, persistência ou processos.

## Como executar

Na raiz do repositório:

```bash
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b12_capstone.py' -v
```

Compare a previsão com cada teste. Registre commit, Python, ambiente, saída e código de retorno; não marque PASS sem observação.

## Refutação reproduzível

Troque evidence.get(name) is not True por not evidence.get(name): test_string_not_pass deve falhar.

Preveja o teste que falhará, faça a alteração temporária, execute e reverta. Caso a mutação sobreviva, trate como lacuna da suíte.

## Transferência

Descreva como vincular cada campo a um log QEMU, commit, artefato e asserção verificável. Um booleano informado manualmente não comprova a execução.

## Evidência e limites

**ENG:** testes do modelo comprovados por execução. **SCI:** previsão e contraexemplo observados. **LEARN:** iniciante resolve caso inédito e explica sem analogia; NOT_RUN até avaliação real. Nenhum resultado aqui demonstra o funcionamento do kernel x86-64.
