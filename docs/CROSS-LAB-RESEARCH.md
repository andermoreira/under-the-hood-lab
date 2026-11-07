# Pesquisa cruzada — decisões de incorporação

Fontes consultadas (READMEs e documentação do proprietário):
- https://github.com/andermoreira/arch-lab — jornada linear, workbooks, referência, auditoria.
- https://github.com/andermoreira/exeattack-lab — onboarding com analogias, glossário, fenômeno → hipótese → observação, capstone.
- https://github.com/andermoreira/crypoattack-lab — par comportamento defeituoso/corrigido, gate duplo.
- https://github.com/andermoreira/llmattack-lab — onboarding de poucos minutos, resultados observáveis, limites de cobertura.
- https://github.com/andermoreira/android-lab — critérios de aceite, testes de integração e falhas induzidas.
- https://github.com/andermoreira/banana — DocDD, critérios de aceite, evidência, NOT_RUN e testes antes de pronto.
- https://github.com/andermoreira/ia — fonte única da verdade, adapters e validação anti-drift.

## Decisões
1. **Adotar** jornada + workbook + referência + implementação, com índice único.
2. **Adotar** analogia explícita e contraexemplo obrigatório.
3. **Adaptar** gate duplo: circuito correto deve passar e mutação intencional deve falhar.
4. **Adotar** evidência com commit, ambiente e saída real.
5. **Adaptar** DocDD: plano de aula/contrato antes da implementação; documentação atualizada após evidência.
6. **Não importar** dependências, políticas de agentes ou código dos labs automaticamente.
7. **Não confundir** resultado do CI com domínio conceitual do estudante.

## Referências externas
- https://www.nand2tetris.org/course — projetos oficiais 1–12.
- https://www.nand2tetris.org/software — simuladores e scripts.
- https://pages.cs.wisc.edu/~remzi/OSTEP/ — sistemas operacionais.

## Próximos incrementos
- Runner HDL oficial headless, com ferramenta/versionamento e comparação .cmp.
- Visualizador de traces de CPU e mapa de memória.
- Runner QEMU/GDB com timeouts e logs serial.
- Exercícios de recuperação ativa e desafios de transferência por módulo.
- Capstone verificável em QEMU.
