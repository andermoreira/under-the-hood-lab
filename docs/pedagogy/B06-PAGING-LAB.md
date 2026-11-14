# B06 — Laboratório executável: tradução de páginas

> **Modelo Python educacional**, não é uma MMU x86-64 nem prova de que o kernel do repositório pagina corretamente. Estado de aprendizagem com alunos: **LEARN NOT_RUN**.

## Objetivo e pré-requisitos

Após a aula [B06](B06-GUIDED.md), diferencie endereço virtual, número da página, deslocamento (offset) e frame físico. Requer Python 3 e terminal básico.

**Analogia:** um prédio pode renumerar apartamentos sem mover o morador; a tabela traduz o número visto pelo visitante para a localização interna. **Limite:** não modela TLB, CR3, níveis de tabelas, privilégio, bits NX, copy-on-write ou page walks reais.

## 1. Preveja antes de executar

Tamanho de página: 4096 bytes (`0x1000`). Tabela: página virtual 2 → frame 7, somente leitura; página virtual 3 → frame 9, gravável.

| Endereço virtual | Página | Offset | Endereço físico esperado |
| --- | --- | --- | --- |
| `0x2005` | 2 | 5 | `0x7005` |
| `0x3000` | 3 | 0 | `0x9000` |
| `0x1000` | 1 | 0 | falha: não mapeada |

Calcule o resultado manualmente: **físico = frame × 4096 + offset**. Exemplo resolvido: `0x2005 = 2 × 4096 + 5`; página 2 aponta para frame 7, portanto `7 × 4096 + 5 = 0x7005`.

## 2. Execute

Na raiz do repositório:

```bash
python3 docs/pedagogy/examples/b06_paging.py
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b06_paging.py' -v
```

A primeira execução deve imprimir dois mapeamentos. O segundo comando deve executar **6 testes**: offset preservado, fronteira, página ausente, escrita proibida, escrita permitida e endereço negativo.

Não marque ENG PASS sem executar e registrar ambiente, commit, saída e código de retorno.

## 3. Experimento negativo controlado

No arquivo `b06_paging.py`, altere temporariamente `frame * PAGE_SIZE + offset` para `frame * PAGE_SIZE`. **Antes de rodar**, preveja o teste que falhará: `test_offset_preserved` (o byte 5 será perdido). Execute os testes, registre a falha e **reverta a mutação**.

Segundo contraexemplo: se retirar a checagem de permissão em `write_address`, o teste `test_readonly_write_fault` deverá falhar.

## 4. Transferência

Sem olhar o código: página virtual 4 → frame 12, gravável. Traduza `0x4ABC`. **Resposta comentada:** offset `0xABC`; endereço físico `0xCABC`. Explique por que o offset não muda.

## 5. Evidências independentes

- **ENG:** testes executados e resultado reproduzível; não inferir sucesso apenas pela existência do arquivo.
- **SCI:** hipótese, previsão, mutação, observação e reversão documentadas.
- **LEARN:** iniciante resolve novo endereço e explica a diferença entre página e frame sem consulta; **NOT_RUN** até avaliação real.

## 6. Próximo passo

Compare a tabela simplificada com o código real de paginação da Trilha B. Liste diferenças antes de tentar adaptar qualquer teste ao kernel. Revisão espaçada em 1, 7 e 30 dias.
