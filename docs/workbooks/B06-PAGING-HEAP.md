# B06 — Paging and page-backed heap

## Previsão (responda antes de ler o código)
1. Se a nova PML4 copiar só as entradas 0–255 e zerar 256–511, o que acontece logo após `mov %0, %%cr3`?
2. Por que copiar só o PML4 não basta para dizer que "o kernel é dono" de todas as tabelas?

## Contract
- Heap: page-sized (4 KiB) allocations from the PMM, accessed through Limine's HHDM, zeroed, with ownership and double-free rejection.
- Paging: map/unmap one private 4 KiB page at `0xffffc00000000000`, with rollback on PMM failure (fault injection, 4 points) and reclaiming only the tables this module created.
- Own address space: `paging_adopt_kernel_space()` allocates a PML4, leaves entries 0–255 (lower half, future user space) empty, copies entries 256–511 (kernel image + HHDM) from Limine and loads CR3. The QEMU gate requires `B06_OWN_PML4_OK` before running the paging tests.

## Evidence (2026-11-07, Docker `ubuntu:24.04` amd64, QEMU 8.2.2, GCC 13.3.0, Limine `v9.x-binary` @ `ee5d29c`)
- Positive: `make test-kernel-boot`, `B04_EXPECT_KEYBOARD=1` and the `#UD` variant print `PASS`.
- Limit case: a second `paging_adopt_kernel_space()` call must fail; the paging tests run with exact PMM accounting on the new CR3.
- Deliberate failure: clearing Present on entries 256–511 → QEMU `Triple fault`, gate `FAIL: kernel did not switch CR3 to its own PML4`.

- #PF negative control: `-DB06_TRIGGER_PF` reads `0x1000`; gate requires `EXCEPTION_PF_CR2_0x0000000000001000` and `EXCEPTION_PF_ERROR_0x0000000000000000` (not-present, read, supervisor). Before the handler existed, the same build produced `Triple fault`.

## Limitations
- Lower levels (PDPT/PD/PT) of the higher half remain **Limine's** tables, which live in bootloader-reclaimable memory: never hand that memory to the PMM until the kernel rebuilds them itself.
- #PF handler (vector 14) is diagnostic only: prints CR2 and the error code, then halts. No demand paging or recovery.
- PMM covers only frames below 4 GiB; the heap is page-granular (no `kmalloc` of small objects); no SMP/TLB shootdown.

## Analogy and where it fails
New PML4 = a new building directory (index) that points to the same floors of the old building. It fails because the CPU caches the old index (TLB): changing the directory does not "erase" what was memorized until CR3 is reloaded/`invlpg`, and the floors still belong to someone else.
