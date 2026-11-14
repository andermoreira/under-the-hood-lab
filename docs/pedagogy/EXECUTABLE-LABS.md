# Índice de laboratórios executáveis — Trilha B

> Estes modelos Python **não são o kernel x86-64**. A aprovação de seus testes é ENG restrito ao modelo, não prova de execução em QEMU, SCI nem LEARN.

## Comece aqui

1. Leia a [jornada guiada](../journey/README.md) e o módulo conceitual correspondente.
2. Anote uma previsão antes de executar cada exemplo.
3. Execute `python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b*.py' -v` na raiz do repositório.
4. Registre commit, versão Python, saída, código de retorno, mutação negativa e sua explicação.
5. Compare com o código real da Trilha B. Não confunda simulação com hardware.

## Módulos disponíveis

| Módulo | Aula prática | Conceito testado |
| --- | --- | --- |
| B05 | [Frames](B05-FRAMES-LAB.md) | first-fit, exaustão, double free |
| B06 | [Paginação](B06-PAGING-LAB.md) | offset, páginas ausentes, permissão |
| B07 | [Scheduler](B07-SCHEDULER-LAB.md) | round-robin, bloqueio |
| B08 | [Syscalls](B08-SYSCALLS-LAB.md) | despacho, argumentos inválidos |
| B09 | [ELF](B09-ELF-LAB.md) | identificador ELF64, fronteiras |
| B10 | [Blocos](B10-BLOCKS-LAB.md) | segmentação, roundtrip |
| B11 | [Shell](B11-SHELL-LAB.md) | parsing, entrada inválida |
| B12 | [Capstone](B12-CAPSTONE-LAB.md) | checklist de evidências, **não comprovação real** |

## Escopo de evidência

- **ENG modelo:** testes Python executados e resultado registrado.
- **ENG kernel:** testes canônicos e logs reais do QEMU; **não inferível dos modelos**.
- **SCI:** hipóteses e controles negativos com resultados observados.
- **LEARN:** avaliação com estudante, sem consulta às respostas; permanece NOT_RUN sem observação.

### Próximas lacunas

Conectar cada modelo a um experimento QEMU com marcador serial e contraexemplo reproduzível; auditar independência da revisão; obter feedback de iniciantes.
