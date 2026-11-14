# Preparação do ambiente para os laboratórios

A primeira experiência de [Comece do zero](START-FROM-ZERO.md) funciona com papel, sem instalar nada. Só prepare o computador quando chegar à parte automatizada.

## Conceitos antes dos comandos

- **Terminal:** janela em que você escreve comandos.
- **Diretório:** pasta de arquivos.
- **Repositório:** conjunto versionado de arquivos do projeto.
- **Python:** linguagem usada em parte dos testes de referência.
- **Make:** ferramenta que executa comandos definidos em um `Makefile`.

## Linux (Debian/Ubuntu)

Em um terminal, instale as dependências básicas:

```sh
sudo apt update
sudo apt install -y git make python3
```

O comando `sudo` exige autorização administrativa. Leia o que será instalado e peça ajuda se estiver usando um computador compartilhado.

## macOS

Verifique se `git`, `make` e `python3` já estão disponíveis. As ferramentas de linha de comando da Apple podem ser instaladas com `xcode-select --install`; Python 3 pode exigir instalação separada. Não assuma que laboratórios Linux x86-64 da Trilha C funcionam diretamente no macOS.

## Windows

Para os primeiros experimentos, use um ambiente Linux via WSL2 ou máquina virtual, seguindo a documentação oficial do sistema. Os comandos de instalação acima se aplicam à distribuição Linux, não ao PowerShell.

## Verifique antes de executar

```sh
git --version
make --version
python3 --version
```

Se algum comando não for encontrado, resolva essa dependência antes de prosseguir.

Após clonar o repositório por um procedimento de sua preferência, entre na pasta que contém o `Makefile` e execute:

```sh
make test
```

Esse comando verifica testes técnicos do projeto; **não comprova que você aprendeu**. Não execute scripts desconhecidos com `sudo`.

**Estado:** guia documental; teste em máquinas de iniciantes `NOT_RUN`.
