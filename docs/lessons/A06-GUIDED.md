# A06 — Endereços, memória e entrada/saída

> Aula complementar. Pressupõe bits, registradores e CPU Hack. LEARN NOT_RUN.

## 1. Problema

Como a CPU pode escrever um valor na RAM e também controlar uma tela usando endereços?

Um **endereço** identifica uma posição em um espaço de memória. **RAM** armazena dados. **I/O mapeado em memória** reserva endereços para interagir com dispositivos.

**Analogia:** apartamentos numerados em um prédio. **Limite:** endereços de dispositivo podem ter efeitos colaterais; não são apenas caixas de armazenamento.

## 2. Modelo da plataforma Hack

Na plataforma Hack do Nand2Tetris, o espaço de dados inclui RAM, tela e teclado. A tela começa em **16384 (SCREEN)**, e o teclado é lido em **24576 (KBD)**. O mapeamento de endereços e os efeitos exatos dependem da especificação Hack; não extrapole isso para computadores x86-64.

| Endereço Hack | Interpretação didática |
| --- | --- |
| 0 | início da RAM de dados |
| 16383 | último endereço da região RAM16K |
| 16384 | início da memória da tela |
| 24575 | último endereço da tela |
| 24576 | registrador de teclado |

A região de tela possui 8192 palavras de 16 bits. Cada palavra representa 16 pixels monocromáticos no modelo Hack.

## 3. Exemplo resolvido

Se o endereço de tela inicial é 16384, a palavra seguinte fica em 16385. Para alcançar a terceira palavra, some 2: **16386**.

**Preveja:** quantos pixels cabem em três palavras de tela? **Resposta:** 48 pixels, pois 3×16=48.

## 4. Experimento sem hardware

```python
def classify(address):
    if 0 <= address < 16384:
        return "RAM"
    if 16384 <= address < 24576:
        return "SCREEN"
    if address == 24576:
        return "KBD"
    return "FORA_DO_MAPA"
for addr in (0, 16383, 16384, 24575, 24576, 24577):
    print(addr, classify(addr))
```

Preveja todas as classificações antes de executar. Este é um **classificador de endereços**, não uma emulação de leitura/escrita de dispositivos.

## 5. Refutação

Altere a condição de tela para `16384 <= address <= 24576`. O endereço 24576 será classificado erroneamente como SCREEN. Qual teste de fronteira denuncia o erro?

## 6. Transferência

Projete um mapa hipotético com 8 posições de RAM, 4 de tela e 1 de teclado, começando em zero, sem sobreposições. Escreva os intervalos e classifique os endereços 7, 8, 11, 12 e 13.

<details><summary>Resposta comentada</summary>

RAM 0–7, tela 8–11, teclado 12; endereço 13 fora do mapa.

</details>

## 7. Limites e revisão

Não confunda endereço de RAM com endereço virtual de processo Linux. Verifique a especificação e os testes da memória Hack antes de declarar equivalência. Explique sem analogia a diferença entre memória comum e I/O mapeado. Revise em 1, 7 e 30 dias.

**ENG/SCI/LEARN: não executados nesta PR editorial.**
