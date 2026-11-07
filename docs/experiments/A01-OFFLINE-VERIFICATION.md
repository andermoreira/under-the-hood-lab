# A01 — Validação independente sem o simulador oficial

## Por quê?
Uma implementação pode parecer correta no papel, mas ter uma conexão errada. Um verificador simples lê as conexões NAND e calcula todas as entradas possíveis.

**Analogia:** o inspetor confere cada fio de uma instalação. Limite: nosso inspetor só entende circuitos combinacionais NAND de um bit, sem tempo, clock, buses ou outros componentes HDL.

## Execute
`python3 tools/verify_hdl.py`

`python3 -m unittest discover -s tests -v`

## Experimento de refutação
O teste `test_mutation_is_detected` substitui XOR por uma rede NAND que calcula OR e exige que o verificador rejeite a tabela. Não é suficiente demonstrar que o circuito correto passa.

## O que foi comprovado?
Somente a consistência das conexões NAND com as tabelas-verdade `.cmp` para Not, And, Or e Xor. **Não** foi comprovada compatibilidade com o simulador oficial nem com circuitos físicos.

## Próximo gate
Executar os mesmos `.tst` com o HardwareSimulator do Nand2Tetris e registrar versão e stdout.
