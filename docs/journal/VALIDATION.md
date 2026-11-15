# Gate LEARN — verificação conservadora

`python3 tools/validate_learn_journal.py docs/journal/B05.md`

O validador lê um diário e aponta campos incompletos: previsão, observação, rubrica nas cinco dimensões e revisões 1/7/30. O diário inicial **deve falhar** com `INCOMPLETE`, pois não houve sessão do estudante.

Mesmo um diário integralmente preenchido só pode receber `READY_FOR_HUMAN_REVIEW`: não há como certificar por texto se a previsão foi anterior ao experimento, se houve independência, nem se os comandos foram executados.

## Gate humano

1. Conferir ordem temporal de previsão e execução.
2. Reproduzir evidências e controles negativos no commit informado.
3. Pedir explicação técnica e transferência para problema novo.
4. Conferir notas 0–3 com justificativa independente.
5. Conferir recuperação ativa após 1, 7 e 30 dias, com datas reais.
6. Registrar aprovação ou rejeição humana separadamente, sem automatizar PASS.

**Não editar diários automaticamente nem gerar evidências fictícias.**
