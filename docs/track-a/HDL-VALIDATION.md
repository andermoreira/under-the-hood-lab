# Evidências HDL — execução no simulador oficial

> **Estado atual: UNVERIFIED.** Merge de fixtures, execução do runner e aprendizagem são eventos diferentes.

## Reprodução

```sh
export N2T_HOME=/caminho/para/nand2tetris
make test-hdl-official 2>&1 | tee hardware-simulator.log
sha256sum hardware-simulator.log
git rev-parse HEAD
```

A rotina `scripts/test-hdl.sh` descobre todos os arquivos `.tst`, executa o simulador e compara saídas com `.cmp`. A verificação estrutural `tests/test_hdl_fixture_integrity.py` **não** comprova comportamento dos chips.

## Registro por execução

| Campo | Evidência |
| --- | --- |
| Commit testado | NOT_RUN |
| Runner e versão do simulador | NOT_RUN |
| URL da execução GitHub Actions | NOT_RUN |
| SHA-256 do log | NOT_RUN |
| Quantidade de testes executados | NOT_RUN |
| Teste negativo comprovado | NOT_RUN |
| Revisão independente | NOT_RUN |
| Resultado ENG | UNVERIFIED |
| Resultado LEARN | NOT_RUN |

## Gate para declarar PASS

1. Executar os fixtures no simulador real com exit code 0.
2. Inspecionar logs e artefatos do mesmo commit, não de commits anteriores.
3. Demonstrar que uma mutação deliberada em um `.cmp` falha e que a reversão volta a passar.
4. Conferir revisão independente.
5. Não alterar o estado LEARN: compreensão exige diário e avaliação humana.

A execução de uma PR não é evidência suficiente para outras PRs após merge sem nova validação do commit final.
