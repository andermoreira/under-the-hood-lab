# F06 — Endereços, ponteiros, páginas e memória física

**Público:** sabe programar, não conhece eletrônica. **Pré-requisito:** [F04-ESTADO-CPU ](F04-ESTADO-CPU.md). **Tempo sugerido:** 60–100 minutos.

## 1. Problema concreto
Memória é um conjunto de posições endereçáveis. Um endereço é um identificador de posição, não o valor armazenado nela. Um ponteiro é um valor usado como endereço segundo as regras da linguagem e do ambiente de execução.

## 2. Conceitos construídos passo a passo
Se cada posição guarda um byte, os endereços 0x1000 e 0x1001 apontam para bytes vizinhos. Uma página de 4096 bytes iniciada em 0x1000 cobre 0x1000 até 0x1FFF inclusive. A página seguinte começa em 0x2000.

## Analogia com o mundo real
A memória é como um prédio de armários numerados: o endereço identifica um armário, e o conteúdo é o objeto guardado. Uma página é um conjunto de armários agrupados em blocos de tamanho fixo. Um mapa de endereços virtuais se parece com um catálogo que aponta para armários físicos.

### Onde a analogia deixa de funcionar
Endereços não são objetos materiais, e páginas podem ter permissões diferentes, estar ausentes ou ser compartilhadas. O catálogo não explica automaticamente cache, TLB, fragmentação ou proteção contra acessos indevidos.

## 3. Exemplo resolvido
O gerenciador de memória física (PMM) controla blocos de memória física, frequentemente chamados frames. O gerenciador de memória virtual cria mapeamentos de páginas virtuais para frames físicos. Endereço virtual não é automaticamente endereço físico; a tradução depende das tabelas de páginas e das permissões.

## 4. Segundo exemplo e caso-limite
Exemplo resolvido: uma região usável começa em 0x1800 e termina antes de 0x4800. Frames completos de 4096 bytes começam em 0x2000 e 0x3000. O primeiro e o último fragmentos não formam frames completos.

## 5. Experimento guiado e leitura do projeto
Em Python, calcule `page=4096`, `start=((0x1800+page-1)//page)*page` e `end=(0x4800//page)*page`; liste `range(start,end,page)` e compare com a resposta. Depois leia `docs/workbooks/B05-PMM.md`.

**Antes de executar:** escreva uma previsão específica. **Depois:** registre comando, saída observada, exit code, commit e explicação para qualquer divergência. Nenhum resultado de execução foi verificado nesta revisão editorial.

## 6. Onde o modelo simplifica
Os exemplos são modelos didáticos. Não extrapole automaticamente de Python para comportamento físico, de Hack para x86-64 ou de uma demonstração para segurança de produção. Identifique o que foi observado e o que permanece hipótese.

## 7. Exercícios progressivos
**Recuperação e aplicação:** Defina byte, endereço, ponteiro, frame, página e mapeamento; explique a diferença entre reservar e zerar memória.

**Transferência:** Se uma região começa em 0x2001 e tem 8192 bytes, quais páginas completas estão dentro dela? Justifique os arredondamentos.

<details>
<summary>Orientações de correção — abra depois de tentar</summary>

Uma resposta satisfatória define os termos com precisão, apresenta pelo menos um exemplo numérico ou operacional, explicita o caso-limite e distingue a evidência executada de uma previsão. Compare sua solução com as definições e exemplos deste capítulo; se houver dúvida, registre a lacuna e busque revisão independente.
</details>

## 8. Evidência e revisão espaçada
**ENG: NOT_RUN** — não há execução de comandos nesta alteração. **LEARN: NOT_RUN** — o estudante ainda não demonstrou entendimento. Revisar sem consulta após **1 dia**, **7 dias** e **30 dias**. Registrar erro inicial, correção e nova tentativa.

[Índice da Trilha 0](../FOUNDATIONS.md)
