# EXP-A01 — Portas NAND

Status: referência Python implementada; HDL NOT_RUN.

Hipótese: NAND é funcionalmente completa.

1. Prever as tabelas-verdade de NOT, AND, OR, XOR.
2. Implementar portas exclusivamente com NAND.
3. Executar `make test`.
4. Implementar equivalentes em HDL Nand2Tetris (pendente).
5. Validar com Hardware Simulator (pendente).
6. Mutação deliberada: XOR=OR deve falhar para A=B=1.

**Evidência necessária:** commit, versão, comandos, logs e arquivos oficiais de comparação HDL.

**Limite:** o modelo Python verifica álgebra booleana, não timing ou comportamento elétrico.
