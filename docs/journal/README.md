# Diário de aprendizagem (Gate LEARN)

Este diretório existe para **exercer o Gate LEARN**, que até a revisão de
novembro de 2026 nunca havia sido preenchido (ver
[`../REVIEW-2026-11.md`](../REVIEW-2026-11.md), achado pedagógico #1).

## Para que serve

O Gate ENG (build e testes) prova que o código funciona. O Gate LEARN prova
que **o estudante aprendeu** — são coisas diferentes, e uma não substitui a
outra. Aqui fica o registro por módulo de:

- **Predição prévia** (antes de ver qualquer solução);
- **Observação** (o que de fato aconteceu ao executar);
- **Rubrica** (nota 0–3 nas cinco dimensões de [`../PEDAGOGY.md`](../PEDAGOGY.md));
- **Datas de revisão espaçada** (1, 7 e 30 dias).

## Regras (do [`../../AGENTS.md`](../../AGENTS.md))

1. A **predição é preenchida pelo estudante antes** de qualquer solução ser
   apresentada. Um arquivo de módulo que começa com a predição em branco é o
   estado correto — não é dívida a ser "resolvida" pela IA.
2. A IA **não preenche** predição, observação nem rubrica. Ela dá pistas
   graduais, gera testes independentes e corrige; não é autora das respostas.
3. Cada conclusão exige evidência executável (comando + saída + commit).
4. Separar sempre hipótese, observação e conclusão.

## Como usar

1. Copie o template abaixo para `docs/journal/<MÓDULO>.md` (ex.: `A01.md`,
   `B05.md`).
2. Preencha **a predição antes** de abrir a solução ou rodar os testes.
3. Rode os testes, cole comando e saída, registre o commit.
4. Compare esperado × observado e dê a nota da rubrica honestamente.
5. Agende as revisões de 1, 7 e 30 dias e volte para registrá-las.

> O ritmo saudável é um módulo por sessão de estudo, não trinta commits em um
> dia. A revisão de novembro observou que A01–B06 foram escritos rápido demais,
> com a IA como autora — o oposto do que este diário corrige.

## Template

Veja [`_TEMPLATE.md`](_TEMPLATE.md).

## Índice de módulos

Os arquivos de diário por módulo já existem (criados a partir do
[`_TEMPLATE.md`](_TEMPLATE.md), com datas de revisão pré-calculadas e **todo o
conteúdo em branco**). As três colunas de estado abaixo são o Gate LEARN em si:
marque cada `☐` quando **você** as cumprir. A IA não as marca por você.

| Módulo | Diário | Previsão feita | Rubrica ≥2 em tudo | Revisões 1/7/30 |
|---|---|---|---|---|
| A01 | [A01](A01.md) | ☐ | ☐ | ☐ |
| A02 | [A02](A02.md) | ☐ | ☐ | ☐ |
| A03 | [A03](A03.md) | ☐ | ☐ | ☐ |
| A04 | [A04](A04.md) | ☐ | ☐ | ☐ |
| A05 | [A05](A05.md) | ☐ | ☐ | ☐ |
| A06 | [A06](A06.md) | ☐ | ☐ | ☐ |
| A07 | [A07](A07.md) | ☐ | ☐ | ☐ |
| A08 | [A08](A08.md) | ☐ | ☐ | ☐ |
| B01 | [B01](B01.md) | ☐ | ☐ | ☐ |
| B02 | [B02](B02.md) | ☐ | ☐ | ☐ |
| B03 | [B03](B03.md) | ☐ | ☐ | ☐ |
| B04 | [B04](B04.md) | ☐ | ☐ | ☐ |
| B05 | [B05](B05.md) | ☐ | ☐ | ☐ |
| B06 | [B06](B06.md) | ☐ | ☐ | ☐ |
| B07 | [B07](B07.md) | ☐ | ☐ | ☐ |
| B08 | [B08](B08.md) | ☐ | ☐ | ☐ |
| B09 | [B09](B09.md) | ☐ | ☐ | ☐ |
| B10 | [B10](B10.md) | ☐ | ☐ | ☐ |
| B11 | [B11](B11.md) | ☐ | ☐ | ☐ |
| B12 | [B12](B12.md) | ☐ | ☐ | ☐ |

Sugestão de ordem (da `REVIEW-2026-11`): comece pelo B05, depois percorra o
resto; a IA corrige e dá pistas, não responde.
