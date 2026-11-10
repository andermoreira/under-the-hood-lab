# F04 — De circuitos sem memória a registradores e CPU

**Público:** sabe programar, não conhece eletrônica. **Pré-requisito:** [F03-PORTAS-CIRCUITOS ](F03-PORTAS-CIRCUITOS.md). **Tempo sugerido:** 60–100 minutos.

## 1. Problema concreto
Um circuito combinacional não lembra o que aconteceu antes. Para contar eventos precisamos de estado: informação que persiste entre instantes de observação. Um registrador guarda bits e pode atualizá-los conforme um sinal de controle e um relógio lógico.

## 2. Conceitos construídos passo a passo
Um registrador de 4 bits contém 0011 (3). Se a lógica calcular +1 e o registrador capturar o resultado na próxima borda de relógio, passará a 0100 (4). Sem a captura, a saída do registrador permanece 0011, mesmo que a lógica combinacional tenha calculado outro valor.

## 3. Exemplo resolvido
Uma CPU combina registradores, uma unidade lógica e aritmética (ALU), lógica de controle e um contador de programa (PC). A ALU calcula; o PC indica a próxima instrução; registradores mantêm operandos e resultados. A CPU Hack da trilha A é um modelo didático, diferente da arquitetura x86-64 da trilha B.

## 4. Segundo exemplo e caso-limite
Exemplo resolvido: PC=7, instrução comum executada sem desvio; PC passa a 8. Se a instrução ordenar salto para 20 e a condição for satisfeita, PC passa a 20. O PC não é um contador de segundos: conta posições de instrução.

## 5. Experimento guiado e leitura do projeto
Modele em Python um registrador `r=3`; calcule `next_r=r+1` sem alterar `r`; em seguida atribua `r=next_r`. Explique a diferença entre calcular o próximo estado e efetivamente armazená-lo.

**Antes de executar:** escreva uma previsão específica. **Depois:** registre comando, saída observada, exit code, commit e explicação para qualquer divergência. Nenhum resultado de execução foi verificado nesta revisão editorial.

## 6. Onde o modelo simplifica
Os exemplos são modelos didáticos. Não extrapole automaticamente de Python para comportamento físico, de Hack para x86-64 ou de uma demonstração para segurança de produção. Identifique o que foi observado e o que permanece hipótese.

## 7. Exercícios progressivos
**Recuperação e aplicação:** Defina estado e combinacional; explique por que um somador sozinho não conta; diferencie ALU, registrador e PC.

**Transferência:** Desenhe um contador de dois bits com estados 00→01→10→11→00. O que acontece se a atualização for desabilitada?

<details>
<summary>Orientações de correção — abra depois de tentar</summary>

Uma resposta satisfatória define os termos com precisão, apresenta pelo menos um exemplo numérico ou operacional, explicita o caso-limite e distingue a evidência executada de uma previsão. Compare sua solução com as definições e exemplos deste capítulo; se houver dúvida, registre a lacuna e busque revisão independente.
</details>

## 8. Evidência e revisão espaçada
**ENG: NOT_RUN** — não há execução de comandos nesta alteração. **LEARN: NOT_RUN** — o estudante ainda não demonstrou entendimento. Revisar sem consulta após **1 dia**, **7 dias** e **30 dias**. Registrar erro inicial, correção e nova tentativa.

[Índice da Trilha 0](../FOUNDATIONS.md)
