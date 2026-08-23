# Arquitetura da Plataforma

Documento vivo — mantido atualizado a cada mudança estrutural. Descreve **como** a
plataforma do curso é construída e servida.

## Visão geral

A plataforma é um **site estático** gerado por **Jupyter Book**, com uma camada de
**notebooks interativos no navegador** (JupyterLite) e uma **bancada Docker** para os
labs pesados. Nada de backend — o estado de progresso vive no navegador
(`localStorage`) e num `progresso.json` versionado.

```{mermaid}
flowchart TD
    A[Conteúdo: .md MyST + .ipynb] --> B[jupyter-book build]
    B --> C[_build/html — site estático]
    C --> D[GitHub Pages via Actions]
    C --> E[JupyterLite / Pyodide<br/>notebooks rodam no browser]
    F[Bancada Docker<br/>JupyterLab + Postgres + DuckDB + MinIO] -.labs pesados.-> A
    G[progresso.json + engajamento.js<br/>streak, badges, mapa vivo] --> C
```

## Componentes

| Componente | Papel | Onde |
|---|---|---|
| **Jupyter Book** | Gera o site navegável (sidebar, busca, tema claro/escuro) | `_config.yml`, `_toc.yml` |
| **JupyterLite** | Kernel Pyodide no browser; roda `pandas`/`numpy`/`duckdb`/`matplotlib` sem instalar | `jupyterlite-sphinx` |
| **Bancada Docker** | Ambiente real de engenharia (o que o Pyodide não roda) | `ambiente/docker-compose.yml` |
| **Correção** | Exercícios "faça o `pytest` passar" + `verificar()` no browser | `modulos/**/exercicio*` |
| **Engajamento** | Streak, badges, mapa vivo, modo 5-min | `_static/engajamento.js`, `dashboard.md`, `progresso.json` |
| **CI/CD** | Build + deploy no GitHub Pages a cada push na `main` | `.github/workflows/deploy.yml` |

## Duas camadas: consumir vs. autorar

- **Consumir (site estático + JupyterLite):** ler teoria e **rodar notebooks no navegador**
  (Pyodide). Edições feitas no JupyterLite ficam só no navegador (IndexedDB) — **não**
  voltam para o repositório. É uma sandbox de leitura/experimentação.
- **Autorar/persistir (JupyterLab da bancada Docker):** o repo é montado no container
  (`../:/home/jovyan/curso`), então **editar ali grava direto nos arquivos** do projeto.
  Este é o caminho para criar conteúdo e persistir (ver o fluxo em `CONTRIBUTING.md`).

## Onde cada notebook roda

Cada notebook **declara** no topo onde deve rodar:

- **Browser (JupyterLite):** fundamentos de Python, pandas, SQL com DuckDB. Zero instalação.
  Pacotes fora do Pyodide (ex.: `duckdb`) são instalados sob demanda via `piplite`.
- **Bancada Docker:** qualquer coisa com Postgres, Airflow, dbt, Spark, MinIO, rede, ou datasets grandes.

Motivo: o Pyodide (WASM) não tem JVM (sem Spark real), não abre conexões TCP a bancos,
e sofre com CORS/arquivos grandes. A *engenharia* de verdade acontece no Docker.

## JupyterLite (notebooks no site)

A extensão `jupyterlite_sphinx` gera, no build, uma instância JupyterLite em
`_build/html/lite/`. Os notebooks do curso (`jupyterlite_contents: modulos/**/*.ipynb`)
são embarcados; cada lab tem um botão **"▶ Rodar no navegador"** que abre o notebook em
`lite/lab/index.html?path=<arquivo>.ipynb`. O build da lite roda junto com o
`jupyter-book build .` (~45s) e é publicado pelo mesmo workflow.

## Fluxo de build (local, Windows)

```bash
pip install -r requirements.txt
jupyter-book build .
# abre _build/html/index.html
```

Recomendado **WSL2 + Docker Desktop** para os labs da bancada.

## Plataforma Astro — pipeline de conteúdo (`plataforma/`)

Front-end de estudos (UI/UX) que **consome o mesmo Markdown do curso** (ver [ADR 0005](docs/decisoes/0005-plataforma-astro.md)).

```{mermaid}
flowchart LR
    MD[modulos/**/*.md + progresso.json] --> SYNC[scripts/sync-conteudo.mjs<br/>transforma MyST + gera índice]
    SYNC --> COL[src/content/aulas/** + src/data/curso.json]
    COL --> ASTRO[astro build<br/>remark-directive + remark-curso]
    ASTRO --> SITE[site estático<br/>Home · Trilha · Módulo · Aula · Painel · Diário]
    LITE[JupyterLite em public/lite] -.iframe nas aulas de lab.-> SITE
```

- **Sync (`npm run sync`, roda antes de `dev`/`build`):** lê `modulos/**` + `progresso.json`, converte as diretivas MyST (`:::{admonition}`, `:::{dropdown}`, ```` ```{mermaid} ````) para a sintaxe `remark-directive`, escreve a coleção `src/content/aulas/` e o índice `src/data/curso.json`.
- **Render:** `remark-directive` + `src/lib/remark-curso.mjs` transformam as diretivas em HTML estilizado com o design system; **mermaid** é renderizado no cliente; **labs** abrem o JupyterLite (iframe em `public/lite`).
- **Páginas geradas:** Trilha e Módulo a partir do `curso.json`; Aula por unidade (conteúdo ou lab). Conteúdo novo no curso → `npm run sync` → aparece sozinho.
- **Gerados (não versionados):** `src/content/aulas/`, `src/data/curso.json`, `public/lite/`, `node_modules/`, `dist/`.

Rodar local: `cd plataforma && npm install && npm run dev` (porta 4321).

## Plataforma Next.js — a plataforma oficial (`web/`)

O front-end de estudos é o app **Next.js** em `web/`, com deploy na **Vercel** (ver
[ADR 0006](docs/decisoes/0006-nextjs-vercel.md)). A versão anterior em Astro foi **removida**.
**Reaproveita o mesmo conteúdo e pipeline:**

- **Next.js (App Router)** em `web/`, SSG, **nosso CSS** portado (Sora+Manrope, verde, claro/escuro, responsivo).
- **Mesmo pipeline de conteúdo:** `web/scripts/sync-conteudo.mjs` lê `modulos/**` + `progresso.json` e gera a coleção + `curso.json` (agora com `cards[]` para flashcards).
- **Render de Markdown:** `react-markdown` + `remark-directive` + `remark-curso` + `rehype-raw`; **mermaid** no cliente; **flashcards** como componente React (modo estudo).
- **JupyterLite** copiado para `web/public/lite` (iframe nas aulas de lab).
- **Build:** `cd web && npm run build` → ~76 páginas estáticas (verificado). **Deploy:** Vercel (Root Directory = `web/`).

> **Papéis atuais:** o **Jupyter Book** permanece como motor de conteúdo e **gerador do JupyterLite** (a instância `lite/` é buildada por ele e copiada para `web/public/lite`); a **plataforma de estudos** é o app **Next.js** (`web/`). O Astro foi aposentado.

## Stack (resumo)

| Camada | Tecnologia |
|---|---|
| Conteúdo (fonte única) | Markdown/MyST em `modulos/**` + `progresso.json` |
| Motor + JupyterLite | Jupyter Book 1.0.3 (Sphinx) + jupyterlite-sphinx (Pyodide + DuckDB WASM) |
| Front-end (plataforma) | Next.js 14 (App Router) + unified/remark-directive/remark-curso/rehype |
| Pipeline | `web/scripts/sync-conteudo.mjs` (Node) |
| Correção | pytest (Python/SQL via DuckDB) |
| Qualidade | `scripts/verificar-conteudo.py` + `referencias.yaml` |
| Bancada de labs | Docker Compose: JupyterLab + Postgres 16 + MinIO; DuckDB; BigQuery (cloud) |
| Deploy | Vercel (plataforma Next) · GitHub Pages (Jupyter Book, opcional) |

## Decisões

As decisões de arquitetura estão registradas como ADRs em [`docs/decisoes/`](docs/decisoes/).

## Convenções de conteúdo

Ver [`CONTRIBUTING.md`](CONTRIBUTING.md) para o padrão de autoria de módulos/unidades
(usa a skill de projeto `autoria-modulo`).
