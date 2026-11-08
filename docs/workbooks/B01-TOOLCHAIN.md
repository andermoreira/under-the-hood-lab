# B01 — Kernel x86-64 freestanding: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## 1. Fenômeno
Um `hello.c` comum compila e roda no Linux. O mesmo arquivo, carregado direto pelo bootloader, não teria `printf`, `main`, libc, sistema de arquivos nem processo. Como construir um executável que não depende de nada disso?

## 2. Previsão (preencher antes de executar)
- O que `-ffreestanding` muda no que o compilador pode assumir?
- Por que o kernel é linkado em `0xffffffff80000000` e o que `-mcmodel=kernel` tem a ver com isso?
- O que acontece no link se `main.c` chamar `printf`?
- Por que o build rejeita instruções BMI2 mesmo compilando sem erro?

## 3. Analogia
Construir o kernel é como montar uma casa num terreno sem rede elétrica nem água: tudo de que a casa precisa vem no próprio caminhão (o ELF).

## 4. Onde a analogia falha
O "terreno" não está vazio: o bootloader (Limine) já criou tabelas de páginas, pilha e modo 64 bits. E o compilador ainda pode emitir chamadas implícitas (`memset`, `memcpy`) que nenhum caminhão trouxe.

## 5. Faça
1. Leia `scripts/build-kernel.sh` e `kernel/x86_64/linker.ld`.
2. Execute `make test-kernel-build` com `LIMINE_HEADER` apontando para um `limine.h` compatível.
3. Rode `readelf -h` e `readelf -l build/kernel/kernel.elf`; anote o tipo, o entry point e os segmentos `PT_LOAD` com suas permissões.

## 6. Refute
- Introduza uma chamada a `printf` numa cópia local: o link deve falhar com `undefined reference`.
- Remova `-mcmodel=kernel` de um arquivo: o que o compilador ou o linker reclamam?
- Retire `-mno-bmi2` de um arquivo e compile com `-march=native`: o gate de BMI2 deve falhar.

## 7. Explique sem analogia
Explique o que o gate B01 comprova (formato ELF x86-64, estático, sem `NEEDED`, sem BMI2) e o que ele não comprova.

## 8. Transfira
Se o kernel precisasse ser carregado em `0xffff800000100000`, que flag de code model você usaria e por quê?

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário.

## 10. Evidência e limites
Gate ENG: `make test-kernel-build` imprime `PASS: freestanding x86-64 kernel ELF built`, local e na CI (job `kernel-build`). O gate B01 comprova **compilação e formato ELF**, não boot no QEMU (isso é o B02). O computador Hack da trilha A é uma arquitetura distinta de x86-64.

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- `-ffreestanding`: o compilador não assume a biblioteca padrão nem que `main` é o ponto de entrada; ainda pode gerar chamadas a `memset`/`memcpy`.
- `-mcmodel=kernel`: assume que código e dados estão nos 2 GiB mais altos, onde endereços cabem em imediatos de 32 bits com extensão de sinal.
- `printf` sem implementação: `undefined reference` no link, porque não há libc.
- BMI2: o compilador obedece ao `-march`; o CPU padrão do QEMU não implementa BMI2 e geraria #UD. Em 11/2026 a CI quebrou porque dois arquivos dependiam do padrão do compilador.
- Transferência: o endereço fica fora dos 2 GiB mais altos; seria preciso `-mcmodel=large`.
</details>
