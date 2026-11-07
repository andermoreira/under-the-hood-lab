# A06 — Computer: CPU, ROM e memória

## Problema
A CPU já sabe interpretar instruções, mas de onde vêm os bits de cada instrução? E onde ficam os dados que ela lê e escreve?

**Analogia:** a ROM é um roteiro de instruções, a CPU é quem executa e a memória é o espaço de trabalho.

**Limites:** ROM e RAM são circuitos endereçados; a CPU busca uma instrução a cada ciclo. O teclado e a tela são periféricos mapeados em endereços, não arquivos.

## Hipótese
O programa `FillRAM.hack` deve executar `@2; D=A; @0; M=D; @5; 0;JMP`: ao fim de seis ciclos, RAM[0] contém 2 e o PC aponta para 5, onde permanece.

## Investigue
1. Observe o caminho PC → ROM32K → instruction → CPU.
2. Observe o caminho CPU (outM/writeM/addressM) → Memory → inM.
3. Em `Memory.hdl`, RAM16K responde a endereços 0–16383, Screen a 16384–24575, Keyboard a 24576.
4. Preveja o que ocorre se o sinal `writeM` não chegar à memória.
5. Rode `python3 -m unittest discover -s tests -v` para o modelo de referência.
6. Com as ferramentas oficiais Nand2Tetris, execute `bash scripts/test-hdl.sh`: o teste `Computer.tst` carrega `FillRAM.hack` na ROM32K, executa seis ciclos e compara RAM[0]=2 e RAM[1]=0. Registre o resultado real antes de afirmar que o HDL funciona.

## Refutação
Desconecte `writeM` e tente executar o programa. O resultado esperado RAM[0]=2 deve deixar de ocorrer.

## Transferência
Explique por que o `pc` possui 15 bits e como endereços de RAM, tela e teclado são selecionados. Diferencie armazenamento de instruções (ROM32K) e armazenamento de dados (RAM16K).

## Evidência
O teste Python **não executa** HDL nem testa chips nativos do simulador. ENG (testes oficiais), SCI (previsões e controles) e LEARN (explicação do aluno) são independentes.
