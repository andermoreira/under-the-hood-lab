# B02 — Boot real e console serial no QEMU

**Pergunta:** um arquivo ELF válido garante que o kernel inicialize? Não.

**Hipótese:** Limine carrega o ELF no QEMU, transfere controle para `kmain` e o kernel imprime `KERNEL_READY` em COM1 (porta 0x3F8).

**Experimento:** `make test-kernel-boot` depois de configurar `LIMINE_HEADER` e `LIMINE_DIR`. Inspecione `build/kernel/serial.log` e o artefato do CI. O teste deve encontrar exatamente uma linha `KERNEL_READY`.

**Controle negativo:** remova a emissão de `KERNEL_READY` e verifique que o gate falha, mesmo se QEMU continuar executando.

**Limites:** `KERNEL_READY` comprova que a entrada do kernel foi alcançada e que o console serial funciona. Ainda não prova interrupções, alocação, isolamento de memória ou execução de processos.
