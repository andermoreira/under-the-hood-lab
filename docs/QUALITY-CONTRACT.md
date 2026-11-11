# Contrato de qualidade pedagógica — piloto

> Estado: **proposta em PR Draft**. A existência deste arquivo não certifica os laboratórios atuais.

## Objetivo

Garantir que cada lição distinga: (1) o programa executou, (2) a evidência demonstra a hipótese e (3) o estudante consegue explicar a causa. São critérios diferentes.

## Checklist por experimento

- [ ] Pré-requisitos, sistema operacional, versões e dependências
- [ ] Hipótese e previsão **antes** da execução
- [ ] Analogia do mundo real **e limite** da analogia
- [ ] Código/comando exato, ambiente e critérios objetivos
- [ ] Resultado esperado, resultado observado, stdout/stderr e exit code
- [ ] Caso negativo que refute interpretação equivocada
- [ ] Explicação causal e distinção entre simulador e implementação real
- [ ] Proveniência: arquivo, commit, referências e revisão independente

## Estados

- `NOT_RUN`: não executado.
- `PASS`: gate objetivo comprovado para o commit e ambiente registrados.
- `FAIL`: execução feita, critério não atendido.
- `UNVERIFIED`: afirmação ou evidência insuficiente.

**PASS de testes não significa revisão semântica nem pedagógica.** A revisão independente deve inspecionar tanto o caso positivo quanto o negativo. Não realizar merge ou deploy com base apenas no parecer do autor ou de uma IA.

## Registro copiável

```yaml
experiment_id: null
commit: null
platform: null
tool_versions: {}
command: null
exit_code: null
expected: null
observed: null
stdout_artifact: null
stderr_artifact: null
negative_control: null
limitations: []
state: NOT_RUN
reviewer: null
reviewed_at: null
```

## Gates e adoção gradual

1. Selecionar **um** laboratório representativo e preencher o registro.
2. Executar a suíte já existente sem alterar sua semântica.
3. Verificar caso negativo, segurança e qualidade da explicação.
4. Revisão independente em commit fixo.
5. Somente após evidência, expandir o contrato aos demais capítulos.

Adoção deste contrato: **NOT_RUN**. Execução do CI neste commit: **NOT_RUN**. Revisão independente: **NOT_RUN**.
