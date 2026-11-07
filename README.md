# Under the Hood Lab

Laboratório educacional do bit ao sistema operacional.

**Trilha A:** NAND → portas lógicas → ALU → memória → CPU Hack → assembler.

**Trilha B:** boot x86-64 → kernel → interrupções → memória virtual → processos → filesystem → shell.

As trilhas são independentes: o kernel x86-64 não roda na CPU Hack.

## Início rápido

```sh
make test
```

O primeiro gate valida o modelo booleano em Python; não substitui testes HDL. Consulte `docs/PEDAGOGY.md`, `docs/ROADMAP.md` e `experiments/hardware/EXP-A01.md`.

## Estado

- [x] Fundamentos, metodologia, analogias e experimento A01
- [x] Testes do modelo de referência NAND-only
- [ ] Circuitos HDL
- [ ] CPU completa
- [ ] Kernel e shell
