# B03 — GDT, IDT e exceção #UD

**Pergunta:** como a CPU transfere controle ao kernel quando encontra uma instrução inválida?

**Hipótese:** com uma GDT de código/dados de kernel e uma IDT contendo a entrada para o vetor 6, `ud2` desvia para um handler que escreve `EXCEPTION_UD_VECTOR_6` no console serial.

**Experimento:** o CI inicializa normalmente e também compila uma variante com `B03_TRIGGER_UD2`. No segundo boot, verifica a presença de `KERNEL_READY` e `EXCEPTION_UD_VECTOR_6`, nessa ordem.

**Controle negativo:** remova o registro da porta IDT 6: o marcador da exceção deve desaparecer e o gate deve falhar.

**Limites:** este marco cobre apenas a exceção #UD e não habilita IRQs externos. Demais vetores, IST/TSS, page faults e recuperação de exceções são trabalho futuro. A rotina de exceção para a CPU deliberadamente.
