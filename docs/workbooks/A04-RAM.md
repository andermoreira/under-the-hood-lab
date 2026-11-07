# A04 — RAM endereçável: quem recebe a escrita?

## Problema concreto
Guardar um valor é útil. Guardar **oito ou 64 valores independentes** exige escolher qual registrador será escrito e qual será lido.

**Analogia:** um armário com gavetas numeradas. O endereço escolhe a gaveta; `load` autoriza substituir seu conteúdo.

**Onde a analogia falha:** a leitura é uma seleção combinacional de sinais; a escrita é sincronizada ao clock, e o hardware não move gavetas.

## Previsão
1. Escreva `0x1234` no endereço 0 e `0xABCD` no último endereço.
2. Desative `load` e apresente `0xFFFF` na entrada do endereço 0.
3. Preveja os valores lidos nos endereços 0, 1 e último.

## Experimento
- RAM8: `DMux8Way` distribui `load` para um dos oito registradores; `Mux8Way16` escolhe a palavra lida.
- RAM64: oito RAM8, com `address[0..2]` para a palavra interna e `address[3..5]` para o banco.
- Execute `python3 -m unittest discover -s tests -v` para a referência Python.
- Execute `bash scripts/test-hdl.sh` com `N2T_HOME` para os testes HDL oficiais.

## Refutação
Force duas gavetas a receber `load` ao mesmo tempo. Que teste de isolamento de endereços falharia?

## Transferência
Calcule quantos bits físicos são armazenados em RAM8 e RAM64. Explique por que a largura do endereço aumenta de 3 para 6 bits.

## Evidência
Modelo Python não valida conexões HDL. Registrar testes oficiais e a diferença entre escrita sincronizada e leitura combinacional.
