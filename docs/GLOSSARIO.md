# Glossário com modelos mentais

| Termo | Definição técnica | Analogia | Limite |
|---|---|---|---|
| Bit | Unidade lógica com dois valores | Interruptor | Níveis elétricos não são interruptores perfeitos |
| NAND | Negação de AND | Portaria com dois sinais | Não interpreta intenção |
| Clock | Sinal de sincronização | Metrônomo | Existem atrasos, skew e setup/hold |
| Registrador | Armazenamento de estado na CPU | Bancada | Não guarda objetos físicos |
| ALU | Circuito de operações lógicas/aritméticas | Calculadora | Não executa programas sozinha |
| ISA | Contrato de instruções visíveis ao software | Vocabulário | Não define toda microarquitetura |
| PC | Registrador do endereço de próxima instrução | Marcador de leitura | Desvios mudam o fluxo |
| Stack | Região e disciplina de memória | Pilha de pratos | ABI define convenções; nem tudo fica na stack |
| ELF | Formato de executável e objetos | Planta de montagem | Loader não segue uma narrativa humana |
| Bootloader | Componente que prepara/carrega o kernel | Chaveiro da oficina | Depende de firmware e protocolo |
| Interrupção | Evento que altera o fluxo de execução | Campainha | Existem máscaras, prioridades e contexto |
| Page fault | Exceção por acesso/tradução de página | Endereço inválido | Também ocorre em paginação legítima |
| Scheduler | Política de seleção de tarefas | Coordenador de turnos | Preempção depende de mecanismos de hardware |
| Syscall | Interface de serviço do kernel | Guichê | Implica fronteira de privilégio |
| Filesystem | Organização persistente de dados | Arquivo de documentos | Durabilidade depende de cache, ordem de escrita e falhas |

Cada módulo deve ampliar este glossário somente com termos efetivamente usados.
