# A08 — Programas executados pelo computador Hack

**Problema:** como demonstrar que assembler, CPU, memória e saltos funcionam juntos?

**Hipótese:** um laço que acumula os números de 5 até 1 deve terminar com RAM[0]=15, RAM[1]=0 e RAM[2]=15.

**Experimento:** execute `make verify` e `make test-hdl-official` com `N2T_HOME` configurado. O runner gera `Sum1To5.hack` a partir do código-fonte e carrega esse binário na ROM do computador.

**Controle negativo:** altere `D;JEQ` para `D;JNE` e confirme que o teste de integração falha.

**Transferência:** mude o contador inicial para 6, calcule o novo resultado esperado (21) e explique o papel do PC, dos saltos e da RAM.

**Limite:** o teste cobre um programa determinístico, não todas as combinações possíveis de instruções nem toda a memória mapeada.
