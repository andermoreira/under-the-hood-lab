# Roadmap (36–48 semanas, 6–8h/semana)

## Trilha A — semanas 1–14

A01 NAND e portas lógicas (tabelas-verdade); A02 MUX, DMUX e somadores; A03 ALU de 16 bits (carry/overflow); A04 registradores e RAM (clock); A05 PC e CPU Hack (trace); A06 memória e I/O; A07 assembler (binário reproduzível); A08 programas próprios (loops e multiplicação).

## Trilha B — semanas 15–48

B01 toolchain freestanding, Limine, linker e QEMU; B02 serial e panic; B03 GDT, IDT e exceções; B04 timer e teclado; B05 alocador físico; B06 paginação e heap; B07 scheduler; B08 ring 3 e syscalls; B09 ELF loader; B10 disco e filesystem; B11 shell; B12 integração e regressão.

## Gates

G1 build; G2 testes unitários; G3 marcador serial KERNEL_READY; G4 ausência de panic inesperado; G5 falhas deliberadas detectadas; G6 commit, versões e logs; G7 reprodução independente.

## Definição de utilizável

Inicializar no QEMU, receber comandos, executar dois programas próprios em modo usuário, ler/gravar arquivos persistentes e conter falhas de programas sem derrubar o kernel.

Fora de escopo inicial: GUI, rede, USB, SMP, hardware físico e POSIX.
