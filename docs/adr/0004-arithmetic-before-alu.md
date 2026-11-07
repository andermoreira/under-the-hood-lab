# ADR 0004 — Construir Add16 antes da ALU

Status: accepted.

O A03 introduz um somador ripple-carry de 16 bits composto por FullAdders já estudados no A02. A saída descarta o carry final, respeitando a interface Add16 do Nand2Tetris.

A ALU Hack será uma etapa posterior e deve receber testes próprios para controles zx/nx/zy/ny/f/no e flags zr/ng. Não inferir correção da ALU a partir de Add16.

A validação Python é uma referência matemática, não execução do HDL. A sintaxe e o circuito HDL exigem teste com HardwareSimulator.
