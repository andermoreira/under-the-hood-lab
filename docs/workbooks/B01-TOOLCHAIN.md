# B01 — Kernel x86-64 freestanding

**Problema:** como construir um executável que não depende de Linux, libc ou runtime do usuário?

**Hipótese:** compilar com `-ffreestanding`, linkar com script próprio e inspecionar o ELF produz um binário x86-64 sem bibliotecas dinâmicas.

**Experimento:** execute `make test-kernel-build` com `LIMINE_HEADER` apontando para um `limine.h` compatível; examine `readelf -h build/kernel/kernel.elf` e `readelf -l`.

**Controle negativo:** remova `-mcmodel=kernel` ou introduza uma chamada a `printf` sem implementação; a compilação/linkedição deve acusar o problema, não ocultá-lo.

**Limites e evidências:** o gate B01 comprova **compilação e formato ELF**, não comprova boot no QEMU. O boot com marcador serial e timeout é o objetivo de B02. O computador Hack da trilha A é uma arquitetura distinta de x86-64.
