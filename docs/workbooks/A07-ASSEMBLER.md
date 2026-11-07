# A07 — Assembler Hack: símbolos viram bits

**Problema:** o computador executa palavras binárias de 16 bits, mas como escrever programas legíveis?

**Analogia (e limite):** um tradutor transforma nomes e instruções em códigos; não executa o programa nem verifica se o algoritmo está correto.

**Hipótese:** se `@HALT` aponta para o rótulo `(HALT)`, o assembler deve usar o endereço ROM da próxima instrução, não consumir uma posição para o rótulo.

**Experimento:**
```bash
python3 tools/hack_assembler.py hardware/nand2tetris/programs/FillRAM.asm -o /tmp/FillRAM.hack
cmp /tmp/FillRAM.hack hardware/nand2tetris/programs/FillRAM.hack
make verify
```

**Controle negativo:** experimente `@32768`, `D=Q` e declarar `(LOOP)` duas vezes; todos devem falhar, não gerar um binário silenciosamente.

**Transferência:** modifique o programa para escrever outro valor em RAM[0], gere o novo binário e descreva como a ROM, o PC, a CPU e a RAM cooperam.

**Limites:** assembler de dois passes com rótulos, símbolos predefinidos e variáveis iniciando em RAM[16]. O simulador oficial continua responsável por validar a execução do HDL.
