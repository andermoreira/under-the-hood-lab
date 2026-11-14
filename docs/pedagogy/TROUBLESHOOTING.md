# Solução de problemas — laboratórios executáveis

> Para iniciantes. **Nenhuma destas instruções altera o kernel.** Os exemplos Python são modelos didáticos.

## Preparação

Abra o terminal na raiz do repositório (a pasta que contém `docs/`). Confirme a versão:

```bash
python3 --version
python3 docs/pedagogy/run_model_tests.py
```

Não é necessário instalar bibliotecas externas para os modelos: eles usam a biblioteca padrão do Python.

## Erros frequentes

### `python3: command not found`

Python 3 não está disponível no PATH. Instale pelo gerenciador de pacotes do seu sistema e confirme `python3 --version`. Não execute scripts obtidos de fontes desconhecidas.

### `No such file or directory`

Você provavelmente está fora da raiz do repositório. Execute `pwd` e `ls docs/pedagogy`. Entre na pasta correta antes de repetir.

### `ModuleNotFoundError: b05_frames`

Execute a suíte por descoberta, em vez de chamar um teste pelo caminho a partir de outra pasta:

```bash
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b*.py' -v
```

### `FAILED (failures=...)` ou `ERROR`

**Não marque PASS.** Identifique o nome do teste e a diferença entre esperado e observado. Reexecute apenas o arquivo relevante com `-p 'test_b07_scheduler.py'` (substitua pelo nome real). Se o teste negativo foi alterado intencionalmente, restaure o código antes de medir o controle positivo.

### Teste passou, mas o kernel falhou

Isso pode acontecer: os modelos não executam o kernel. Consulte [protocolo QEMU](QEMU-EVIDENCE-PROTOCOL.md) e rode os gates canônicos do repositório. Um resultado Python verde não é evidência de boot ou persistência.

## Como pedir ajuda sem perder a investigação

Registre (1) capítulo, (2) comando exato, (3) previsão, (4) saída e código de retorno, (5) ambiente/versão e (6) o que tentou. O facilitador deve orientar a formular hipótese antes de fornecer a solução.

## Checklist de saída

- Consegue explicar o conceito em palavras próprias?
- Previu a saída antes de executar?
- Interpretou um teste falhando?
- Resolveu um caso diferente do exemplo?
- Sabe o que o modelo **não** prova?

**LEARN permanece NOT_RUN** até observação de um iniciante real; uma checklist preenchida pelo autor não substitui avaliação independente.
