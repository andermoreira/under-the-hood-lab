# B05 — Alocador de frames físicos: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## 1. Fenômeno
A máquina tem 128 MiB de RAM, mas parte dela é do firmware, do kernel e do próprio bootloader. Como o kernel descobre quais páginas físicas de 4 KiB pode usar e entrega cada uma uma única vez?

## 2. Previsão (preencher antes de executar)
- Por que o PMM nunca entrega o frame físico 0, e o que quebraria se entregasse?
- Quantos bytes ocupa um bitmap que cobre 4 GiB em frames de 4 KiB?
- Uma região usável começa em `0x1800` e tem `0x3000` bytes. Quais frames inteiros ela contém?
- Para que serve o bitmap `owned`, além de `used`?

## 3. Analogia
O PMM é o guarda-volumes de uma rodoviária: um quadro com um pino por armário, livre ou ocupado, e só se devolve o armário com o tíquete certo.

## 4. Onde a analogia falha
O "quadro" (bitmap) mora na própria memória que ele controla, e os armários não estão vazios ao serem entregues: o conteúdo antigo continua lá até alguém zerar. Também não há "tíquete": a devolução é validada só pelo endereço.

## 5. Faça
1. Leia `kernel/x86_64/pmm.c` e o trecho B05 de `kmain`.
2. Rode `make test-kernel-boot` e confira `B05_PMM_ALLOC_FREE_OK`.
3. Calcule à mão o tamanho de `used` e `owned` e confirme com `nm -S build/kernel/kernel.elf`.

## 6. Refute
- Remova a checagem de `owned` em `pmm_free` numa cópia: qual teste de `kmain` deveria falhar? Ele falha?
- Faça `pmm_init` liberar também regiões não usáveis: preveja o que acontece no boot.

## 7. Explique sem analogia
Explique o arredondamento de início (para cima) e de fim (para baixo) das regiões, o cursor de próxima busca e por que `UINT64_MAX` sinaliza falta de memória.

## 8. Transfira
O PMM cobre só os primeiros 4 GiB. O que mudaria para cobrir 64 GiB, e quanto custaria o bitmap?

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário.

## 10. Evidência e limites
Gate ENG: `B05_PMM_ALLOC_FREE_OK` no boot, local e na CI (aloca dois frames distintos, libera um, rejeita double free). Limites: só frames abaixo de 4 GiB; busca linear; sem zerar páginas; memória "bootloader reclaimable" nunca é devolvida (ainda contém as tabelas de páginas do Limine).

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- Frame 0: endereço físico 0 é indistinguível de "nulo" em muitas APIs e, em PCs, contém a tabela de vetores do modo real e dados do BIOS. `pmm_free` também rejeita 0, então os dois lados são consistentes.
- 4 GiB / 4 KiB = 1 Mi frames → 1 Mi bits = 128 KiB por bitmap (256 KiB com `owned`).
- `0x1800`–`0x4800`: os frames inteiros são `0x2000` e `0x3000` (o primeiro e o último parciais ficam fora).
- `owned` distingue "ocupado porque foi alocado" de "ocupado porque nunca foi usável": impede liberar memória do firmware ou do kernel.
- Transferência: 16 Mi frames → 2 MiB por bitmap; aí compensa um bitmap por região ou uma lista de livres.
</details>
