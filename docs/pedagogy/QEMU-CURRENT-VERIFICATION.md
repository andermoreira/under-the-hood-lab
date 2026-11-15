# Verificação atual do kernel QEMU — estado e procedimento

## Estado auditável

- Histórico: `docs/REVIEW-2026-11.md` documenta boots reais e mutações de B07–B12 em 2026-11-10.
- Implementação: `scripts/test-kernel-boot.sh` inicia QEMU e verifica marcadores B05–B12.
- CI: `.github/workflows/tests.yml` possui job `kernel-boot`, boot normal, teclado, #UD e #PF.
- Verificação posterior às PRs #100/#101: **UNVERIFIED**. Não atribuir PASS sem artefatos da execução atual.
- O backlog `QEMU-VALIDATION-BACKLOG.md` começou em NOT_RUN por projeto; isso não apaga a evidência histórica documentada.

## Reproduzir no Linux com Docker

```sh
make verify-kernel-docker
python3 tools/verify_qemu_serial.py build/kernel/serial.log --output build/kernel/serial-evidence.json
```

Atenção: o container do Makefile monta o repositório em `/work`; confira permissões e arquivos gerados no host.

## Verificar na CI

1. Abra Actions → workflow `gates` → run do commit auditado.
2. Confirme o job `kernel-boot` e os quatro cenários (normal, teclado, #UD, #PF).
3. Baixe `b02-qemu-boot-evidence` e registre hash SHA-256 do artefato, commit, versões e run URL.
4. Confirme `build/kernel/serial-evidence.json` com `status=PASS` e compare os marcadores ao log original.
5. Introduza mutação controlada em branch isolada e demonstre gate vermelho; reverta e demonstre verde.
6. Solicite revisão independente antes de registrar ENG kernel como PASS para o novo commit.

## Registro

| Campo | Valor |
| --- | --- |
| Commit atual auditado | NOT_RUN |
| URL do workflow | NOT_RUN |
| QEMU e toolchain | NOT_RUN |
| Serial e hash | NOT_RUN |
| Controle negativo | NOT_RUN |
| Revisão independente | NOT_RUN |
| Resultado atual | UNVERIFIED |

Não confundir verificação estática, execução de modelos Python, boot do kernel e aprendizagem do estudante.
