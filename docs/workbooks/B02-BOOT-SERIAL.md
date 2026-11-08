# B02 — Boot real e console serial: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## 1. Fenômeno
O B01 produziu um ELF válido. Isso garante que o kernel inicializa? Ainda não sabemos se alguma instrução dele chegou a executar.

## 2. Previsão (preencher antes de executar)
- Quem lê o ELF, carrega os segmentos e salta para `kmain`?
- Como o Limine encontra as requisições do kernel (`base_revision`, HHDM, memmap) dentro do binário?
- Por que usar a porta serial COM1 (`0x3F8`) e não a tela?
- O que `serial_write` espera antes de enviar cada byte?

## 3. Analogia
O serial é um telégrafo: o kernel bate um caractere de cada vez e o QEMU anota tudo num arquivo (`serial.log`).

## 4. Onde a analogia falha
Não há operador do outro lado: o kernel consulta um bit de status do UART (LSR bit 5, transmissor vazio) e o QEMU nunca descarta caracteres por "pressa". E o marcador não prova nada além de "esta linha de código foi alcançada".

## 5. Faça
1. Leia `kmain` e `serial_init` em `kernel/x86_64/main.c`.
2. Execute `make test-kernel-boot` com `LIMINE_HEADER` e `LIMINE_DIR` configurados.
3. Abra `build/kernel/serial.log` e localize `KERNEL_READY`; confira que `scripts/test-kernel-boot.sh` usa timeout e exige a linha exata.

## 6. Refute
Remova a emissão de `KERNEL_READY` numa cópia: o gate deve falhar mesmo com o QEMU continuando a executar. Depois, quebre o bit de status em `serial_write` (espere pelo bit errado) e observe o que acontece com o log.

## 7. Explique sem analogia
Descreva a cadeia firmware → Limine → `kmain` → UART 16550 → arquivo do QEMU, e por que o gate usa timeout em vez de esperar o QEMU terminar.

## 8. Transfira
Como você provaria que o kernel chegou a uma linha específica se não houvesse porta serial?

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário.

## 10. Evidência e limites
Gate ENG: `make test-kernel-boot` imprime `PASS: QEMU booted Limine and emitted KERNEL_READY on COM1`, local e na CI (job `kernel-boot`). `KERNEL_READY` comprova que a entrada do kernel foi alcançada e que o console serial funciona; não prova interrupções, alocação, isolamento de memória ou processos.

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- O Limine lê o ELF, carrega os `PT_LOAD`, monta as tabelas de páginas e salta para o entry point.
- As requisições ficam entre os marcadores `.limine_requests_start` e `.limine_requests_end`; o Limine procura os IDs mágicos e preenche `response`.
- O serial é simples (algumas portas de I/O) e o QEMU grava a saída em arquivo: dá para testar sem tela.
- `serial_write` espera o bit 5 do LSR (`0x3F8 + 5`) indicar que o registrador de transmissão está vazio.
- Transferência: escrever num endereço de memória e inspecionar pelo monitor do QEMU, ou usar a porta de debug `0xE9`, ou provocar uma saída do QEMU com código conhecido.
</details>
