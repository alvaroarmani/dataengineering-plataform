# ADR 0006 — Plataforma em Next.js + deploy na Vercel

- **Status:** Aceito (branch `plataforma-nextjs`)
- **Data:** 2026-08-22

## Contexto

A plataforma foi construída em Astro (ADR 0005). O usuário optou por **Next.js** com deploy
na **Vercel** — familiaridade com React, ecossistema, deploy nativo, e a porta aberta para
**backend depois** (API routes: progresso sincronizado, login). Feito em **branch separada**
para preservar a versão Astro (que permanece no `main`).

## Decisão

Reimplementar o front-end em **Next.js (App Router)** em `web/`, **reaproveitando**:
- o **conteúdo Markdown** do curso (`modulos/**`) — fonte única, intocada;
- os **plugins** `preprocess-myst.mjs` + `remark-curso.mjs`;
- a instância **JupyterLite** (gerada pelo Jupyter Book) via iframe;
- o **design system** (CSS portado para `app/globals.css`).

**Arquitetura do conteúdo:** o `scripts/sync-conteudo.mjs` **compila Markdown → HTML no build**
(unified: remark-parse + gfm + directive + remark-curso + rehype-raw) e grava `src/data/curso.json`.
As páginas Next apenas exibem (`dangerouslySetInnerHTML`), e mermaid roda no cliente.

## Consequências

- ✅ Deploy nativo na Vercel; base para features com backend (progresso real, auth) no futuro.
- ✅ Paridade com o Astro (Home, Trilha, Módulo, Aula, Painel, Diário, flashcards de virar, tema claro/escuro, JupyterLite).
- ✅ Conteúdo continua vindo de `modulos/**` — escrever Markdown basta; o sync propaga.
- ⚠️ Dois front-ends no repo por ora (Astro no `main`, Next na branch). Decidir depois qual manter.
- ⚠️ O deploy em si exige a conta do usuário (Vercel + GitHub) — não automatizável aqui.
