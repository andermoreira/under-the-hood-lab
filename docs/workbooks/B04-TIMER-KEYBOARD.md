# B04 — Timer PIT e teclado PS/2: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## 1. Fenômeno
O kernel precisa saber que o tempo passou e que uma tecla foi apertada, sem ficar perguntando o tempo todo. Como um dispositivo interrompe a CPU?

## 2. Previsão (preencher antes de executar)
- Por que o PIC 8259 precisa ser remapeado para os vetores `0x20`–`0x2f`?
- O que acontece se o handler do timer esquecer de enviar EOI (`outb(0x20, 0x20)`)?
- Com divisor 11932, quantas interrupções por segundo o PIT gera?
- Por que o stub em assembly salva `rax`, `rcx`, `rdx`, `rsi`, `rdi` e `r8`–`r11`, mas não `rbx`?

## 3. Analogia
O PIC é uma recepcionista: recebe chamadas de vários aparelhos e avisa a CPU uma de cada vez, por ordem de prioridade.

## 4. Onde a analogia falha
A recepcionista não sabe quando a conversa acabou: o kernel precisa avisar (EOI). Sem isso, o PIC nunca mais entrega aquela linha. E a "chamada" interrompe a CPU no meio de qualquer instrução seguinte, sem pedir licença.

## 5. Faça
1. Leia `kernel/x86_64/devices.c` e o macro `IRQ_ENTRY` em `interrupts.S`.
2. Rode `make test-kernel-boot` e confira `B04_PIC_PIT_READY` e `B04_TIMER_TICKS_OK` (cinco IRQs reais).
3. Rode `B04_EXPECT_KEYBOARD=1 bash scripts/test-kernel-boot.sh`: o script injeta uma tecla pelo monitor do QEMU e exige `B04_KEYBOARD_IRQ`.

## 6. Refute
- Remova o EOI do timer numa cópia: preveja se `B04_TIMER_TICKS_OK` aparece e confira.
- Mascare o IRQ1 (`outb(0x21, 0xfe)`): o gate de teclado deve falhar.

## 7. Explique sem analogia
Descreva o caminho de uma tecla: controlador PS/2 → IRQ1 → PIC → vetor 33 → stub → `irq_keyboard_handler` → EOI → `iretq`.

## 8. Transfira
Para medir 1 ms em vez de 10 ms, que divisor você usaria no PIT? Qual o custo de interromper 10 vezes mais?

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário.

## 10. Evidência e limites
Gate ENG: boot normal e boot com teclado imprimem `PASS`, local e na CI. O driver só reporta scancodes crus: sem mapa de teclas, buffer, APIC, USB ou SMP. O boot negativo `#UD` continua obrigatório.

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- Remapeamento: por padrão, IRQ0–7 caem nos vetores 8–15, que colidem com exceções da CPU (8 é double fault).
- Sem EOI: o PIC não entrega novas IRQs dessa linha; o contador para em 1 e `B04_TIMER_TICKS_OK` nunca aparece.
- 1193182 / 11932 ≈ 100 Hz.
- Registradores: os da lista são caller-saved na ABI SysV; `rbx`, `rbp` e `r12`–`r15` são preservados pela função C chamada (o stub salva `r12` porque o usa).
- Transferência: 1193182 / 1000 ≈ 1193; dez vezes mais entradas no kernel, mais tempo de CPU gasto só com o tick.
</details>
