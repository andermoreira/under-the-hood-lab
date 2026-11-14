# Laboratórios de linha de comando — prever, executar, refutar

> Experimentos em **modelos Python**. Eles não iniciam QEMU e não provam comportamento do kernel.

## Preparação

Execute na raiz do repositório:

```bash
python3 --version
python3 docs/pedagogy/run_model_tests.py
```

Registre o commit e o código de saída. Antes de cada comando, escreva a previsão.

## B05 — Quem possui um frame?

Preveja a sequência de alocações, o ponto de exaustão e o frame devolvido após liberação.

```bash
python3 docs/pedagogy/examples/b05_experiment_cli.py \
  --frames 2,4,6 --ops alloc,alloc,alloc,alloc,free:4,alloc
```

Explique a diferença entre `EXHAUSTED` e `INVALID_FREE`. Faça um segundo teste com `--frames 1 --ops alloc,free:1,free:1`.

## B06 — Por que uma leitura pode passar e a escrita falhar?

O tamanho de página no modelo é 4096 bytes. A página virtual 2 aponta para frame 7, somente leitura; a página 3 aponta para frame 9, gravável.

```bash
python3 docs/pedagogy/examples/b06_experiment_cli.py \
  --map 2:7:ro,3:9:rw \
  --requests read:8197,write:8197,write:12288,read:0
```

Antes de executar, calcule o endereço físico de 8197. Identifique qual operação falha por permissão e qual falha por ausência de mapeamento.

## B10 — O que um checksum prova?

```bash
python3 docs/pedagogy/examples/b10_experiment_cli.py --text "abcdefghi" --block-size 4
python3 docs/pedagogy/examples/b10_experiment_cli.py --text "abcdefghi" --block-size 4 --drop-last
```

Compare hashes, integridade e códigos de saída. Explique por que recuperar bytes em memória não prova durabilidade após reboot.

## Registro e transferência

Copie o [template de experimento](EXPERIMENT-RECORD-TEMPLATE.md) e registre comandos, previsão, saída, controle negativo e interpretação. Depois altere os parâmetros para um caso novo, sem consultar a solução. Consulte [solução de problemas](TROUBLESHOOTING.md) se a execução falhar.

## Limites da evidência

| Dimensão | O que estas CLIs podem apoiar | O que não provam |
| --- | --- | --- |
| ENG modelo | cálculo, estado e detecção de falhas dos simuladores | execução do kernel |
| ENG kernel | nada por si só | boot, MMU real, persistência |
| SCI | previsão e controle negativo, se registrados | hipótese testada sem logs |
| LEARN | atividade didática | aprendizagem medida sem avaliação |

Todos os estados começam **NOT_RUN** até execução e revisão. Para QEMU, consulte [backlog de validação real](QEMU-VALIDATION-BACKLOG.md).
