# B10 — Disco e sistema de arquivos: observe, preveja, construa e refute

**Não consulte o gabarito antes de tentar.**

## 1. Fenômeno
A RAM é apagada ao desligar, mas um arquivo salvo continua lá na próxima vez. Como o kernel conversa com um disco (que fala em "setores", não em "arquivos") e, em cima desses setores crus, cria a ilusão de arquivos com nome e conteúdo que persistem?

## 2. Previsão (preencher antes de executar)
- O driver ATA PIO lê um setor escrevendo o LBA em portas e depois lendo 256 palavras de 16 bits. Por que 256 palavras, e por que é preciso esperar o bit de status antes de ler?
- O sistema de arquivos guarda um "superbloco" no LBA 0. Para que serve o número mágico `UTHLABFS`, e o que o kernel faz se não o encontrar?
- Para reescrever um arquivo, dois setores diferentes são gravados. Quais, e por quê?
- Por que o teste regenera a imagem do disco a cada execução?

## 3. Analogia
O disco é um arquivo de gavetas numeradas (setores). O sistema de arquivos é a etiqueta na primeira gaveta (diretório) que diz "o arquivo X está nas gavetas 5 a 7". Ler um arquivo é consultar a etiqueta e abrir as gavetas certas.

## 4. Onde a analogia falha
As "gavetas" têm tamanho fixo e indivisível (512 bytes): um arquivo de 3 bytes ainda ocupa uma gaveta inteira. E não há gaveta "meio aberta" — toda leitura/escrita é de uma gaveta completa, mesmo para mudar um byte. A etiqueta (diretório) também mora numa gaveta do próprio arquivo, então atualizar o tamanho de um arquivo exige regravar a gaveta da etiqueta.

## 5. Faça
1. Leia `kernel/x86_64/ata.c`, `fs.c`, o gerador `tools/make_disk.py` e o bloco B10 de `kmain`.
2. Rode `python3 tools/make_disk.py /tmp/d.img` e inspecione os primeiros bytes (`od -A x -t x1z /tmp/d.img | head`).
3. Rode `make test-kernel-boot` e confirme `B10_FS_OK`.

## 6. Refute
- Numa cópia, faça `fs_write` pular a gravação do setor de dados: o reread ainda confere? (Controle negativo verificado: boot falha com "disk read/write persistence smoke test not observed".)
- Corrompa o número mágico do superbloco na imagem: o que `fs_read` retorna?
- Peça um arquivo inexistente: o loader distingue "não achei" de "achei vazio"?

## 7. Explique sem analogia
Explique sem gavetas: o handshake de portas do ATA PIO (LBA, contagem, comando, polling de BSY/DRQ), a diferença entre ler o diretório e ler os dados, e por que a persistência só é provada relendo do disco após uma nova transação, não da RAM.

## 8. Transfira
Hoje cada arquivo tem capacidade fixa e cabe em um setor. O que precisaria mudar para arquivos maiores que um setor, e depois para arquivos que crescem (fragmentação, lista de blocos ou alocação por extensões)?

## 9. Revisão
Sem consulta, refaça as previsões da seção 2 após 1 dia, 7 dias e 30 dias. Registre data e acertos no seu diário (`docs/journal/B10.md`).

## 10. Evidência e limites
Gate ENG: `B10_FS_OK` no boot, local e na CI (lê o arquivo semeado `disk-v1`, reescreve para `disk-v2!`, relê do disco e confirma). O disco IDE é anexado ao QEMU com `-machine pc` (PIIX, IDE legacy em 0x1F0). Limites: ATA PIO só (sem DMA/IRQ), 28-bit LBA, um único drive; FS de diretório plano, capacidade fixa por arquivo, caminho de leitura/escrita limitado a um setor (512 B); sem permissões, timestamps nem gerência de espaço livre.

<details>
<summary>Gabarito parcial — abra somente após tentar</summary>

- 256 palavras de 16 bits = 512 bytes = um setor; espera-se o bit DRQ/DRDY porque o disco só tem os dados prontos depois de processar o comando.
- Magia `UTHLABFS`: confirma que a gaveta 0 é mesmo um superbloco deste FS; sem ela, `fs_read` recusa (retorna -1) em vez de interpretar lixo como diretório.
- Reescrever grava: (1) o setor de dados do arquivo e (2) o setor do diretório, para atualizar o campo `size`.
- Regenerar a imagem: a run anterior reescreveu `disk-v1`→`disk-v2!`; sem regenerar, a asserção inicial "leu disk-v1" falharia na segunda execução.
</details>
