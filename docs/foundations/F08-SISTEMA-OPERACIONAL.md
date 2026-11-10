# F08 — Por que um sistema operacional existe?

**Público:** sabe programar, não conhece eletrônica. **Pré-requisito:** [F06-ENDERECOS-MEMORIA ](F06-ENDERECOS-MEMORIA.md). **Tempo sugerido:** 60–100 minutos.

## 1. Problema concreto
Dois programas querem usar CPU, memória e dispositivos. Sem regras de isolamento, um pode sobrescrever dados do outro ou controlar hardware arbitrariamente. Um sistema operacional fornece mecanismos de execução, proteção e acesso mediado a recursos.

## 2. Conceitos construídos passo a passo
Um processo é uma instância de programa em execução com estado e recursos associados. O escalonador escolhe qual tarefa pode usar a CPU. Memória virtual ajuda a separar espaços de endereços. Uma chamada de sistema (syscall) é um mecanismo controlado para solicitar serviços privilegiados.

## 3. Exemplo resolvido
Exemplo resolvido: um programa quer escrever na saída. Em vez de acessar diretamente o dispositivo, solicita ao kernel uma operação de escrita. O kernel valida parâmetros e executa a ação permitida. Isso não garante segurança automaticamente: a implementação da validação é essencial.

## 4. Segundo exemplo e caso-limite
Kernel e shell não são sinônimos. O kernel gerencia recursos; o shell é uma interface que recebe comandos e solicita serviços. Um sistema pode ter kernel sem shell, e diferentes shells podem conversar com o mesmo kernel.

## 5. Experimento guiado e leitura do projeto
Compare os capítulos `docs/workbooks/B07-SCHEDULER.md`, `B08-USERMODE.md` e `B11-SHELL.md` e identifique responsabilidades. Se algum arquivo estiver indisponível, registre a lacuna em vez de presumir seu conteúdo.

**Antes de executar:** escreva uma previsão específica. **Depois:** registre comando, saída observada, exit code, commit e explicação para qualquer divergência. Nenhum resultado de execução foi verificado nesta revisão editorial.

## 6. Onde o modelo simplifica
Os exemplos são modelos didáticos. Não extrapole automaticamente de Python para comportamento físico, de Hack para x86-64 ou de uma demonstração para segurança de produção. Identifique o que foi observado e o que permanece hipótese.

## 7. Exercícios progressivos
**Recuperação e aplicação:** Defina processo, escalonamento, isolamento, syscall, kernel e shell. Explique o que uma chamada de sistema não autoriza automaticamente.

**Transferência:** Desenhe a sequência de uma solicitação de escrita de usuário ao kernel e indique três pontos em que uma validação pode falhar.

<details>
<summary>Orientações de correção — abra depois de tentar</summary>

Uma resposta satisfatória define os termos com precisão, apresenta pelo menos um exemplo numérico ou operacional, explicita o caso-limite e distingue a evidência executada de uma previsão. Compare sua solução com as definições e exemplos deste capítulo; se houver dúvida, registre a lacuna e busque revisão independente.
</details>

## 8. Evidência e revisão espaçada
**ENG: NOT_RUN** — não há execução de comandos nesta alteração. **LEARN: NOT_RUN** — o estudante ainda não demonstrou entendimento. Revisar sem consulta após **1 dia**, **7 dias** e **30 dias**. Registrar erro inicial, correção e nova tentativa.

[Índice da Trilha 0](../FOUNDATIONS.md)
