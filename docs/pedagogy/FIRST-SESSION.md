# Primeira sessão guiada — do conceito ao experimento

> Roteiro para um estudante sem experiência prévia com sistemas operacionais. Duração estimada: 30–45 minutos. **LEARN NOT_RUN** até avaliação real.

## O que você vai descobrir?

Por que o computador precisa controlar quais partes da memória estão livres? Imagine um estacionamento com vagas numeradas. Cada carro ocupa uma vaga; liberar uma vaga que não pertence ao carro pode causar conflito. **Limite da analogia:** frames são unidades de memória física, não lugares fixos para carros; o sistema também lida com regiões reservadas, permissões e endereços virtuais.

## 1. Prepare o ambiente

Abra o terminal na raiz do projeto. Confira:

```bash
python3 --version
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b05_frames.py' -v
```

Se aparecer erro, consulte [solução de problemas](TROUBLESHOOTING.md). Não avance sem entender se o comando executou ou falhou.

## 2. Preveja antes de testar

Há três frames livres: 2, 4 e 6. Um alocador sempre escolhe o menor livre. Responda **antes** de ler a solução:

1. Quais serão as três primeiras alocações?
2. O que acontece na quarta?
3. Se você liberar o frame 4, qual será o próximo escolhido?
4. Por que liberar o frame 4 duas vezes deve produzir erro?

## 3. Execute o exemplo

```bash
PYTHONPATH=docs/pedagogy/examples python3 - <<'PY'
from b05_frames import FrameAllocator, OutOfFrames
a = FrameAllocator([2, 4, 6])
print([a.alloc() for _ in range(3)])
try:
    a.alloc()
except OutOfFrames:
    print("sem frames livres")
a.release(4)
print(a.alloc())
PY
```

Registre a saída, compare com sua previsão e explique a diferença se houver.

## 4. Controle negativo

Abra uma cópia local de `docs/pedagogy/examples/b05_frames.py`. Remova temporariamente a proteção de double-free em `release`. Execute:

```bash
python3 -m unittest discover -s docs/pedagogy/examples -p 'test_b17_memory_ownership.py' -v
```

Preveja qual teste deveria ficar vermelho. **Reverta a alteração** e execute novamente. Nunca trate um teste vermelho como aprovação.

## 5. Transferência

Sem consultar o exemplo, resolva este cenário: frames disponíveis são 1, 5, 8 e 10; duas alocações acontecem, depois o primeiro frame é liberado e uma terceira alocação ocorre. Liste a sequência e explique o que muda se o alocador usar outra política de escolha.

## 6. Verifique a compreensão

Você consegue explicar o que significa “frame livre”, “frame alocado”, “exaustão” e “double-free” sem usar a metáfora do estacionamento? Consegue apontar **duas limitações** deste simulador em relação ao PMM do kernel?

## Solução comentada (leia somente após tentar)

As alocações são 2, 4 e 6; a quarta falha por exaustão. Após liberar 4, ele volta a ser o menor frame disponível e será escolhido. A liberação duplicada é rejeitada para evitar que um frame já livre seja tratado como propriedade de outra alocação. No exercício de transferência, a sequência é 1, 5, depois 1 novamente. Outra política pode escolher ordem diferente, mas não deve alocar simultaneamente o mesmo frame para dois donos.

## Evidências

**ENG modelo:** depende de testes executados. **ENG kernel:** requer QEMU. **SCI:** exige previsão e controle negativo observados. **LEARN:** exige observação independente do estudante, não uma afirmação do autor.
