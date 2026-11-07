# Auditoria pedagógica e técnica

## Rubrica (0 a 3)
0 = ausente; 1 = com muita ajuda; 2 = independente em caso conhecido; 3 = independente em caso novo.

| Critério | Evidência |
|---|---|
| Fenômeno primeiro | Pergunta observável antes da definição |
| Analogia honesta | Mapeamento explícito e seção de limites |
| Predição ativa | Resposta registrada antes do teste |
| Construção incremental | Passos pequenos e código inspecionável |
| Refutação | Teste negativo que realmente detecta defeito |
| Observabilidade | Saída, registradores, logs ou traces |
| Explicação formal | Sem recorrer à analogia |
| Transferência | Problema novo não resolvido no tutorial |
| Recuperação ativa | Exercícios em 1/7/30 dias |
| Reprodutibilidade | Ambiente, comando, exit code, commit |

## Gates separados
- ENG: build, testes e integração.
- SCI: hipótese falsificável, controle negativo, limites e evidência.
- LEARN: previsão, explicação e transferência com rubrica >=2 em cada dimensão.

## Antipadrões proibidos
- Teste verde apresentado como prova de aprendizagem.
- Gabarito antes da tentativa.
- Analogia sem apontar onde falha.
- Resultado inventado ou não executado marcado como PASS.
- Diagramas sem experimento reproduzível.
- Tutorial que salta pré-requisitos.
- Alterar o contrato para fazer um teste passar sem documentar a mudança.
- Copiar código de outro lab sem verificar licença e compatibilidade.

## Recibo de experimento
Registrar: commit, ambiente, ferramentas/versões, comandos, exit code, esperado, observado, evidência, limitações e os três gates.
