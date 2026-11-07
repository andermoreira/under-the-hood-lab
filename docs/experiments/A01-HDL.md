# EXP-A01-HDL — NAND → NOT e AND

**Estado inicial: NOT_RUN até execução com simulador oficial.**

## Pergunta
Uma única primitiva NAND é suficiente para implementar NOT e AND?

## Analogia
Uma portaria nega apenas quando dois sinais estão presentes. Repetir a entrada A nas duas portas de entrada produz NOT(A).

**Limite:** a portaria não descreve propagação elétrica nem temporização.

## Antes de rodar
Preveja as saídas de NOT(0), NOT(1), AND(0,0), AND(0,1), AND(1,0) e AND(1,1). Registre em seu caderno.

## Execute
1. Obtenha a distribuição oficial em https://www.nand2tetris.org/software
2. Extraia localmente e aponte N2T_HOME para a pasta que contém `HardwareSimulator.sh` ou `tools/HardwareSimulator.sh`.
3. Execute `bash scripts/test-hdl.sh`.
4. Registre versão, commit, comando, saída e exit code.

O runner retorna **2** quando a ferramenta não está disponível; isso significa NOT_RUN, não PASS.

## Falha deliberada
Em uma cópia local de `And.hdl`, remova a segunda NAND e ligue a saída da primeira diretamente à saída do chip. O teste deve detectar o erro. Reverta a mutação.

## Transfira
Implemente OR apenas com NAND sem copiar a resposta. Explique usando álgebra booleana.

## Gates
- ENG: scripts Not e And passam no simulador oficial.
- SCI: hipótese, controle negativo e evidência.
- LEARN: explicação sem analogia e exercício de transferência.

**Nota:** a suíte Python é um modelo independente; não substitui a validação HDL.
