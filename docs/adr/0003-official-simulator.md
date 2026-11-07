# ADR 0003 — Simulador oficial como oráculo de HDL

Status: accepted.

A trilha de hardware usa a sintaxe HDL do Nand2Tetris e os testes .tst/.cmp. A implementação Python permanece um modelo lógico independente. Não considerar um circuito validado somente porque a referência Python passa.

O simulador oficial deve ser instalado explicitamente; o projeto não distribui seus binários nem faz downloads silenciosos. Ausência da ferramenta gera NOT_RUN (exit 2).

Próximo passo: fixar versão/checksum e integrar a ferramenta à CI depois de validar os scripts localmente.
