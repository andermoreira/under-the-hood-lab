# A07 — Do Assembly Hack aos bits

> Aula complementar. Pressupõe A05 e A06. LEARN NOT_RUN.

## 1. Problema concreto

Humanos preferem escrever `@5` a memorizar uma sequência de 16 bits. Como transformar uma instrução legível em um padrão que a CPU Hack reconheça?

**Assembly:** representação simbólica de instruções. **Assembler:** programa que converte essas instruções em código de máquina. **ISA:** contrato que define instruções válidas.

**Analogia:** traduzir uma notação de partitura em comandos. **Limite:** o assembler segue regras exatas de codificação, não interpreta intenção humana.

## 2. Exemplo resolvido: instrução A

Na ISA Hack, uma A-instruction tem 16 bits: o bit mais alto é 0 e os 15 restantes representam um valor não negativo.

```text
@5
0 000000000000101
= 0000000000000101
```

`@5` carrega o valor 5 no registrador A. **Não** significa necessariamente ler o conteúdo de RAM[5]; isso depende da instrução seguinte.

## 3. Preveja

Traduza `@0`, `@1` e `@16` para 16 bits. Confira com:

```python
for n in (0, 1, 5, 16):
    print(f"@{n} -> {n:016b}")
```

Esse programa cobre **somente instruções A numéricas válidas**, não instruções C, rótulos ou variáveis. A faixa numérica de A-instruction é 0 a 32767.

## 4. Rótulos e endereços

Em um programa Hack:

```asm
(LOOP)
@LOOP
0;JMP
```

O rótulo `(LOOP)` aponta para o endereço ROM da próxima instrução real. Ele não ocupa uma palavra ROM. Neste exemplo, `LOOP` vale 0 e o programa executa um salto incondicional para o início.

## 5. Teste negativo

Uma tradução ingênua conta `(LOOP)` como instrução ROM. Preveja o endereço errado que resultaria. Explique por que um assembler precisa de uma passagem para localizar rótulos.

## 6. Transferência

```asm
@3
(AGAIN)
@AGAIN
0;JMP
```

Qual é o endereço de `AGAIN`? Quais palavras ocupam ROM 0, ROM 1 e ROM 2?

<details><summary>Dica</summary>

Rótulos não consomem ROM; cada A-instruction e C-instruction consome uma palavra.

</details>

<details><summary>Resposta comentada</summary>

`AGAIN` vale 1. ROM 0 contém `@3`, ROM 1 contém `@1` e ROM 2 contém a instrução C `0;JMP`.

</details>

## 7. Conexão e limites

Compare as previsões com o assembler e os testes do repositório. O exemplo não ensina ainda a codificação de todos os campos de C-instruction: consulte a especificação da ISA Hack. Explique sem analogia a diferença entre rótulo, endereço e valor.

Revisão em 1, 7 e 30 dias. **ENG/SCI/LEARN: não executados nesta PR editorial.**
