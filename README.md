# Especialização em Engenharia de Dados

Plataforma de um programa autodirigido, no padrão de uma pós-graduação *lato sensu*, para
migrar de carreira e ficar pronto para o mercado de **Engenharia de Dados**.

> **Não é** um curso credenciado nem emite diploma com validade legal. O valor está na
> competência real e no portfólio construído. Ver [`ppc/apresentacao.md`](ppc/apresentacao.md).

## O que é isto

Um site de curso (**Jupyter Book**) com teoria, **notebooks interativos** (JupyterLite),
correção automática de exercícios (**pytest**) e uma **bancada Docker** para labs reais.
16 disciplinas · 5 eixos · ~550h · TCC = um Data Warehouse completo.

## Como rodar o site localmente

```bash
pip install -r requirements.txt
jupyter-book build .
# abra _build/html/index.html
```

## Como subir a bancada de trabalho (labs)

```bash
cd ambiente
cp .env.example .env
docker compose up -d
```

Detalhes em [`ambiente/README.md`](ambiente/README.md).

## Estrutura do repositório

| Caminho | O quê |
|---|---|
| `intro.md`, `_toc.yml`, `_config.yml` | Capa e configuração do Jupyter Book |
| `ppc/` | Projeto Pedagógico (apresentação, objetivos, matriz, TCC, bibliografia…) |
| `modulos/` | As 15 disciplinas (ementa + teoria + labs + exercícios) |
| `projetos/` | Projetos integradores por eixo (portfólio) |
| `tcc/` | Especificação do Data Warehouse (TCC) |
| `ambiente/` | Bancada Docker (JupyterLab + Postgres + MinIO) |
| `datasets/` | Catálogo de datasets reais |
| `dashboard.md`, `progresso.*`, `_static/engajamento.js` | Camada de engajamento (streak, mapa vivo) |
| `metodo-de-aprendizado.md`, `plano-de-estudos.md`, `diario.md` | Método e apoio ao aluno |
| `ARCHITECTURE.md`, `CONTRIBUTING.md`, `docs/decisoes/` | Documentação viva (arquitetura + ADRs) |
| `.claude/skills/autoria-modulo/` | Skill de projeto para autoria consistente |

## Documentação

- Arquitetura: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- Guia de autoria: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Decisões (ADRs): [`docs/decisoes/`](docs/decisoes/)
- Histórico: [`CHANGELOG.md`](CHANGELOG.md)
