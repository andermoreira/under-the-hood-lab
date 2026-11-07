# Atlas de analogias

| Conceito | Mundo real | Onde a analogia falha |
|---|---|---|
| NAND | Portaria que só nega quando duas autorizações coincidem | Bits não têm intenção; a saída é função lógica determinística |
| Clock | Metrônomo de uma fábrica | Circuitos têm propagação e restrições de setup/hold |
| Registradores | Bancada de trabalho | Não são objetos móveis; são elementos de estado digital |
| CPU | Operário lendo cartões de instrução | Instruções têm formatos e efeitos elétricos precisos |
| RAM | Prédio com apartamentos numerados | Endereços virtuais podem ser traduzidos, cacheados ou inválidos |
| Stack | Pilha de bandejas | Stack é região de memória com convenções de ABI |
| Interrupção | Campainha que chama um atendente | Prioridades, máscaras e contexto são controlados por hardware/software |
| Scheduler | Coordenador de turnos | Preempção depende de timer e salvamento de contexto |
| Memória virtual | Endereço interno de um condomínio | Mapeamentos podem ser compartilhados e ter permissões |
| Syscall | Guichê de atendimento | Transição de privilégio é mecanismo da CPU |
| Filesystem | Arquivo de pastas e documentos | Durabilidade depende de blocos, cache e consistência |
| Bootloader | Chaveiro que abre a oficina | Firmware e bootloader obedecem protocolos específicos |

## Protocolo

Para cada analogia: desenhar correspondências; produzir dois exemplos em que ajuda; produzir um contraexemplo; substituir a analogia por um modelo técnico; testar a transferência do conhecimento.
