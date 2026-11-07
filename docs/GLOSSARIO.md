# Glossário ilustrado por analogias — Under the Hood Lab

Este glossário é uma **ponte para a compreensão**, não um substituto da definição formal. Em cada termo: **o que é → analogia → onde falha → como verificar**.

## 1. Bits e circuitos

| Conceito | Definição técnica | Analogia cotidiana | Onde a analogia falha | Experimento |
|---|---|---|---|---|
| Bit | Valor lógico binário, 0 ou 1 | Interruptor desligado/ligado | Sinais físicos têm tensão, ruído e transições | A01 |
| Porta lógica | Circuito que implementa função booleana | Regra de uma portaria | Não interpreta regras humanas; calcula saídas | A01 |
| NAND | NOT(AND(A,B)); só retorna 0 para A=B=1 | Portaria que nega quando duas condições coincidem | Não há intenção nem interpretação | A01 |
| NOT | Inverte um bit | Interruptor inversor | A saída tem atraso de propagação | A01 |
| AND | 1 apenas se ambas entradas forem 1 | Duas chaves em série | Circuitos reais têm características elétricas | A01 |
| OR | 1 se ao menos uma entrada for 1 | Dois acionadores alternativos | Não equivale a soma aritmética | A01 |
| XOR | 1 se entradas forem diferentes | Detector de divergência | Para mais de duas entradas, representa paridade, não “apenas um” | A01 |
| Tabela-verdade | Enumeração das combinações de entradas e saídas | Tabela de decisões | Não descreve temporização nem consumo | A01 |
| Completude funcional | Capacidade de compor qualquer função booleana | Alfabeto capaz de formar mensagens | Não implica eficiência de portas | A01 |
| MUX | Seleciona uma entre entradas conforme bits de seleção | Chave seletora de canais | Não move fisicamente dados | A02 |
| Somador | Circuito que calcula soma binária e carry | Caixa registradora | Carry e overflow não são a mesma coisa | A02 |
| Carry | Transporte de bit para posição superior | Vai-um da aritmética | Overflow de inteiros com sinal exige outra análise | A02 |
| Overflow | Resultado não representável na largura/tipo adotados | Odômetro que dá a volta | Depende da interpretação com/sem sinal | A03 |
| ALU | Unidade combinacional de operações lógicas e aritméticas | Calculadora interna | Não executa programa nem controla memória sozinha | A03 |
| Clock | Sinal periódico usado para coordenar estado | Metrônomo | Há skew, jitter e requisitos de setup/hold | A04 |
| Flip-flop | Elemento sequencial que mantém estado | Interruptor que memoriza posição | Estado é elétrico e sensível à temporização | A04 |

## 2. CPU, memória e programas

| Conceito | Definição técnica | Analogia | Onde falha | Experimento |
|---|---|---|---|---|
| Registrador | Armazenamento pequeno e rápido acessível à CPU | Bancada de trabalho | Não é uma caixa física movida pelo operador | A04 |
| RAM | Memória endereçável de leitura e escrita | Prédio de apartamentos numerados | Endereços virtuais podem ser traduzidos | A04 |
| Endereço | Identificador de posição em espaço de memória | Número de apartamento | Nem todo endereço é válido ou físico | A04 |
| CPU | Unidade que busca, decodifica e executa instruções | Operário seguindo cartões | CPUs modernas têm paralelismo e especulação | A05 |
| ISA | Contrato das instruções visíveis ao software | Vocabulário da máquina | Não define como circuitos internos são construídos | A05 |
| Program Counter (PC) | Registrador que indica a próxima instrução | Marcador de página | Desvios, exceções e saltos alteram o fluxo | A05 |
| Assembly | Representação simbólica de instruções de máquina | Notação de uma partitura | Não é linguagem universal entre ISAs | A07 |
| Assembler | Traduz assembly em código de máquina | Tradutor de símbolos | Não é compilador geral de alto nível | A07 |
| Stack | Área de memória usada conforme convenções de pilha | Pilha de pratos | Layout depende de ABI, otimizações e arquitetura | Ponte/B08 |
| Heap | Área de alocação dinâmica | Depósito de objetos | Não é necessariamente uma região contígua | B06 |
| ABI | Convenções binárias de chamadas e dados | Protocolo entre equipes | É contrato técnico com detalhes de registradores/alinhamento | Ponte |
| ELF | Formato de objetos e executáveis | Planta de montagem | Loader interpreta segmentos e metadados, não narrativa | B09 |

## 3. Sistema operacional

| Conceito | Definição técnica | Analogia | Onde falha | Experimento |
|---|---|---|---|---|
| Firmware | Código de inicialização da plataforma | Rotina de abertura de uma oficina | Não é necessariamente parte do SO | B01 |
| Bootloader | Prepara ambiente e carrega kernel | Chaveiro que abre a oficina | Depende de protocolo e firmware | B01 |
| Kernel | Núcleo privilegiado que gerencia recursos | Administração de um prédio | Hardware impõe fronteiras de privilégio | B01 |
| Interrupção | Evento que desvia execução para handler | Campainha | Existem prioridades, máscaras e contexto | B03 |
| Exceção | Evento síncrono gerado durante execução | Alarme por violação de regra | Não é necessariamente erro recuperável | B03 |
| Page fault | Exceção de tradução/permissão de página | Porta sem autorização | Também pode ser parte normal de paginação | B06 |
| Memória virtual | Espaço de endereços traduzido/protegido | Endereço interno de condomínio | Mapeamentos podem ser compartilhados | B06 |
| Scheduler | Política que escolhe qual tarefa executar | Coordenador de turnos | Preempção requer mecanismo de contexto | B07 |
| Context switch | Troca do estado de execução entre tarefas | Troca de operador na bancada | Envolve registradores e possivelmente espaço de endereços | B07 |
| Ring 3 | Nível de privilégio de usuário em x86 | Área de acesso restrito | É mecanismo de CPU, não apenas regra administrativa | B08 |
| Syscall | Entrada controlada do usuário em serviço do kernel | Guichê de atendimento | Há instruções, ABI e transição de privilégio | B08 |
| Filesystem | Organização de arquivos e metadados em armazenamento | Arquivo de documentos | Consistência depende de escrita, cache e falhas | B10 |
| Shell | Interface para interpretar comandos | Recepcionista | Pode executar processos, redirecionar fluxos etc. | B11 |

## 4. Ferramentas e evidência

| Termo | Significado | Como verificar |
|---|---|---|
| HDL | Linguagem de descrição de hardware; aqui, sintaxe Nand2Tetris | Simulador oficial |
| .tst / .cmp | Script de teste e saída esperada do simulador | HardwareSimulator |
| QEMU | Emulador/virtualizador usado para executar o kernel x86-64 | Boot e logs serial |
| GDB | Depurador para inspecionar estado e fluxo | Breakpoints, registradores, memória |
| Teste de mutação | Alteração intencional para verificar se testes detectam defeitos | Mutante deve ser rejeitado |
| PASS | Gate executado com sucesso | Comando, exit code, evidência |
| FAIL | Gate executado e reprovado | Erro e diagnóstico |
| NOT_RUN | Gate ainda não executado | Não confundir com PASS |
| ENG / SCI / LEARN | Correção técnica / validade experimental / aprendizagem demonstrada | Três avaliações separadas |

## Como estudar um termo

1. Descreva-o com suas palavras usando a analogia.
2. Identifique **duas limitações** da analogia.
3. Faça uma previsão observável.
4. Execute o experimento associado.
5. Explique novamente sem a analogia.
6. Resolva um caso novo sem consultar o gabarito.

Este glossário deve crescer junto com os experimentos; termos ainda não implementados são **orientação curricular**, não evidência de funcionalidade.
