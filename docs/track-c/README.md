# Trilha C — Low-Level Programming

> **Estado:** proposta implementada parcialmente. C01 possui código e testes; C03–C12 estão em desenvolvimento, não laboratórios validados. Não confundir ENG com LEARN.

## Por quê?

Complementar a Trilha A (CPU Hack) e a Trilha B (kernel próprio x86-64) com programas reais em Linux x86-64. A CPU Hack **não** executa os programas desta trilha; o kernel da Trilha B **não** é Linux e não implementa automaticamente a ABI Linux.

Inspiração temática: [Programação em Baixo Nível Descomplicada (PBND), Blau Araújo](https://bolha.dev/blau_araujo/pbnd). Exercícios e textos próprios, sem reproduzir materiais de terceiros.

## Pré-requisitos

Linux x86-64, GNU binutils (as, ld, objdump, readelf), make, Python 3; gdb e strace opcionais. Em ARM64/macOS, use uma VM Linux x86-64: não execute diretamente o binário ELF x86-64. Não rode binários desconhecidos como root.

## Roteiro

| Lab | Tema | Evidência esperada | Estado |
| --- | --- | --- | --- |
| C01 | Instruções, registradores e write/exit | saída exata, código de retorno, disassembly | Implementado; execução local não verificada |
| C02 | ELF: seções, segmentos, símbolos, entry point | readelf/objdump e mapa anotado | Implementado; CI pendente |
| C03 | Syscalls: read, write, openat e erros | strace e teste de falha | Implementado; CI pendente |
| C04 | echo, cat e wc simplificados | comparação com casos de referência | NOT_RUN |
| C05 | ABI System V AMD64 e C/Assembly | chamada cruzada, stack alinhada | NOT_RUN |
| C06 | Stack, heap, mmap e memória virtual | mapas de memória e hipóteses | NOT_RUN |
| C07 | Flags, aritmética, bitwise e overflow | testes de fronteira | NOT_RUN |
| C08 | Buffers, I/O e custos de syscalls | benchmark reproduzível | NOT_RUN |
| C09 | Debugging com GDB e falhas intencionais | backtrace e causa-raiz | NOT_RUN |
| C10 | /proc, /sys e observabilidade | evidências de origem dos dados | NOT_RUN |
| C11 | Linking estático/dinâmico e libc | inspeção de dependências | NOT_RUN |
| C12 | Ponte Linux ↔ kernel B | matriz de requisitos e lacunas, sem alegar compatibilidade | NOT_RUN |

## Contrato pedagógico por laboratório

1. **Prever:** formular hipótese antes de executar.
2. **Construir:** menor implementação com código comentado.
3. **Observar:** registrar comandos, saídas, arquitetura e versões.
4. **Quebrar:** provocar falha controlada e explicar seu mecanismo.
5. **Validar:** casos positivos, negativos e teste automatizado.
6. **Conectar:** apontar componentes correspondentes nas trilhas A/B e diferenças de ISA/ABI.
7. **Revisar:** distinguir ENG (gates técnicos) de LEARN (registro do estudante). Usar [contrato de qualidade](../QUALITY-CONTRACT.md).

## C01 — primeiro laboratório

Veja [C01](C01.md), [C02](C02.md) e [C03](C03.md). Execute `make -C labs/low-level/C01 test` em Linux x86-64. O teste verifica o resultado funcional e a presença de instruções; não certifica aprendizagem, segurança nem equivalência ao kernel próprio.

## Ponte com a Trilha B

B08 fornece mecanismo próprio de entrada de syscall, B09 carrega ELF64 e B12 isola falhas de ring 3. Isso **não** garante que binários Linux rodem no kernel B. Compare formato ELF, endereçamento, syscalls, argumentos, convenções e carregamento; liste divergências antes de qualquer tentativa de execução.
