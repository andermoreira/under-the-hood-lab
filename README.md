# Under the Hood Lab

Laboratório educacional do bit ao sistema operacional.

**Trilha A:** NAND → portas lógicas → ALU → memória → CPU Hack → assembler.

**Trilha B:** boot x86-64 → kernel → interrupções → memória virtual → scheduler → ring 3 e syscalls → carregador ELF → disco e filesystem → shell.

As trilhas são independentes: o kernel x86-64 não roda na CPU Hack.

A trilha B atinge a "Definição de utilizável" do roadmap: inicia no QEMU, recebe comandos pelo shell, executa dois programas próprios em modo usuário, lê/grava arquivos persistentes e contém falhas de programas sem derrubar o kernel.

## Navegação pedagógica

- [Jornada guiada](docs/journey/README.md)
- [Glossário com analogias e experimentos](docs/GLOSSARIO.md)
- [Guia para iniciantes](docs/INICIANTE.md)
- [Workbook A01](docs/workbooks/A01.md)
- [Diário de aprendizagem (Gate LEARN)](docs/journal/README.md)

## Início rápido

```sh
make test
```

O primeiro gate valida o modelo booleano em Python; não substitui testes HDL. Consulte `docs/PEDAGOGY.md`, `docs/ROADMAP.md` e `experiments/hardware/EXP-A01.md`.

## Estado (2026-11-10, `main` @ a3eaf88 + dívida técnica fechada)

Gate ENG = build e testes executados (local e CI). Gate LEARN = registro do estudante (previsão, rubrica, revisões); o diário já existe em [docs/journal/](docs/journal/README.md), mas **ainda não foi exercido em nenhum módulo**.

| Módulo | Conteúdo | ENG | LEARN |
|---|---|---|---|
| A01–A02 | NAND, portas, MUX, somadores | PASS (Python + simulador oficial na CI) | aberto |
| A03 | Add16 e ALU Hack | PASS | aberto |
| A04 | Bit, Register, RAM8, RAM64 | PASS | aberto |
| A05–A06 | PC, CPU Hack, Computer | PASS | aberto |
| A07–A08 | assembler e programas | PASS | aberto |
| B01–B04 | toolchain, boot serial, GDT/IDT/#UD, PIT e teclado | PASS (QEMU na CI) | aberto |
| B05 | alocador de frames físicos | PASS | aberto |
| B06 | heap de páginas, kmalloc, PML4 própria, #PF | PASS | aberto |
| B07 | scheduler cooperativo round-robin (ring 0) | PASS (QEMU) | aberto |
| B08 | ring 3, GDT/TSS, SYSCALL/SYSRET | PASS (QEMU) | aberto |
| B09 | carregador ELF64 de programas de usuário | PASS (QEMU) | aberto |
| B10 | disco ATA PIO e filesystem persistente | PASS (QEMU) | aberto |
| B11 | shell do kernel (ls, cat, write, run) | PASS (QEMU) | aberto |
| B12 | integração e contenção de falha de ring 3 | PASS (QEMU) | aberto |

Achados das revisões técnica e pedagógica, e o que falta corrigir: [docs/REVIEW-2026-11.md](docs/REVIEW-2026-11.md).
