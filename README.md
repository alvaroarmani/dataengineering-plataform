# Especialização em Engenharia de Dados

Plataforma de um programa autodirigido, no padrão de uma pós-graduação *lato sensu*, para
migrar de carreira e ficar pronto para o mercado de **Engenharia de Dados**.

> **Não é** um curso credenciado nem emite diploma com validade legal. O valor está na
> competência real e no portfólio construído. Ver [`ppc/apresentacao.md`](ppc/apresentacao.md).

## O que é isto

Um curso com teoria, **notebooks interativos** (JupyterLite), **correção automática** de
exercícios (**pytest**, inclusive SQL via DuckDB) e uma **bancada Docker** para labs reais.
16 disciplinas · 5 eixos · ~550h · TCC = um Data Warehouse completo.

**Fonte única, uma plataforma:** o conteúdo vive em Markdown (`modulos/**`); o **Jupyter Book**
é o motor de conteúdo + gerador do JupyterLite, e a **plataforma de estudos** (UI/UX) é o app
**Next.js** em `web/` (deploy na Vercel). Ver [`ARCHITECTURE.md`](ARCHITECTURE.md) e
[ADR 0006](docs/decisoes/0006-nextjs-vercel.md). _(A versão anterior em Astro foi aposentada.)_

## Estado atual (2026-08-22)

- ✅ **Eixo 1 (conteúdo) completo:** M1 Fundamentos · M2 Linux/Git/Docker · M3 Python (6 unidades) · M4 SQL (6 unidades) + **projeto integrador do Eixo 1** (`projetos/eixo-1-fundamentos/`).
- ✅ **Plataforma Next.js oficial** (Astro removido); build gera ~76 páginas; pipeline de conteúdo e JupyterLite funcionando.
- ⏳ Em andamento: Eixo 2 (Modelagem/DW/dbt) — M5 iniciado. Próximo: deploy na Vercel.

## Como rodar

**Motor de conteúdo (Jupyter Book):**
```bash
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
python scripts/verificar-conteudo.py   # linter de conteúdo
jupyter-book build .                    # abre _build/html/index.html
```

**Plataforma Next.js (`web/`):**
```bash
cd web
npm install
npm run dev     # http://localhost:3000   (roda o sync do conteúdo antes)
npm run build   # build estático para a Vercel
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
| `projetos/` | Projetos integradores por eixo (Eixo 1 com `starter/` de portfólio) |
| `tcc/` | Especificação do Data Warehouse (TCC) |
| `web/` | Plataforma **Next.js** (App Router) — a plataforma oficial; deploy na Vercel |
| `referencias.yaml`, `scripts/verificar-conteudo.py` | Registro de fontes + linter de conteúdo |
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
