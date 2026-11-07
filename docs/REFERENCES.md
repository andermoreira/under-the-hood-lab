# Referências fundamentais e uso no laboratório

As referências orientam a aprendizagem; não substituem experimentos, testes ou evidências.

## Três pilares

1. **Charles Petzold — Code: The Hidden Language of Computer Hardware and Software (2ª ed., 2022).**
   - Livro: https://www.charlespetzold.com/books/
   - Circuitos interativos: https://www.codehiddenlanguage.com/Chapter00/
   - Uso: fenômenos, modelos mentais, analogias e limites das analogias em A01–A04 e na introdução à CPU.
   - Não reproduzir capítulos ou ilustrações protegidas.

2. **Noam Nisan e Shimon Schocken — The Elements of Computing Systems (2ª ed.).**
   - Projetos e materiais oficiais: https://www.nand2tetris.org/
   - Ferramentas: https://www.nand2tetris.org/software
   - Uso: contratos HDL, projetos de hardware, linguagem de máquina, assembler, VM e software Hack.
   - HardwareSimulator é a autoridade para a execução de HDL; o verificador offline cobre apenas um subconjunto.

3. **Remzi H. Arpaci-Dusseau e Andrea C. Arpaci-Dusseau — Operating Systems: Three Easy Pieces (OSTEP).**
   - Livro gratuito oficial: https://pages.cs.wisc.edu/~remzi/OSTEP/
   - Uso: Track B — processos/virtualização, concorrência e persistência, associados a experiências com QEMU/GDB e kernel x86-64.
   - Não confundir o sistema operacional educacional Hack com o kernel x86-64.

## Mapeamento pedagógico

| Etapa | Conceitos de Code | Projetos de TECS/Nand2Tetris | OSTEP |
|---|---|---|---|
| A01: NAND e portas | Relés e portas lógicas | Projeto 1 | Não se aplica |
| A02: MUX e somadores | Aritmética com portas | Projeto 2 | Não se aplica |
| A03: Add16 e ALU | Aritmética automatizada e ALU | Projeto 2 | Não se aplica |
| A04: Bit e Register | Feedback, clock e memória | Projeto 3 | Não se aplica |
| A05–A08: CPU, assembly, programas | Registradores, sinais de controle, saltos | Projetos 4–6 | Não se aplica |
| B01–B12: kernel x86-64 | Ponte conceitual entre hardware e SO | Comparação, não implementação Hack | Processos, memória, concorrência e persistência |

## Como usar cada referência

Para cada workbook: indicar leitura **por tema**, nunca exigir a compra de livro para concluir um exercício; formular previsão antes do código; executar teste e controle negativo; registrar limites da analogia e evidências. Sempre oferecer o material gratuito oficial quando houver.

## Ferramentas e documentação adicional

- https://wiki.osdev.org/
- https://wiki.osdev.org/Limine_Bare_Bones
- https://www.qemu.org/docs/master/system/gdb.html
- https://os.phil-opp.com/
