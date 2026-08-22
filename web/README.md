# Plataforma de estudos — Next.js (branch `plataforma-nextjs`)

Front-end da Especialização em Engenharia de Dados em **Next.js (App Router)**, para deploy
na **Vercel**. Reaproveita o conteúdo do curso (`../modulos`), os plugins remark e o
JupyterLite. Veja o [ADR 0006](../docs/decisoes/0006-nextjs-vercel.md).

## Rodar local

```bash
cd web
npm install
npm run dev      # roda o sync do conteúdo e sobe o Next em http://localhost:3000
```

- `npm run sync` — compila `../modulos/**` → `src/data/curso.json` e copia o JupyterLite para `public/lite`.
- `npm run build` — sync + `next build` (SSG).

> **Pré-requisito do JupyterLite:** o `public/lite` é copiado de `../_build/html/lite`. Se
> ainda não existir, gere-o antes com o Jupyter Book na raiz do projeto:
> `./.venv/Scripts/jupyter-book.exe build .` (ou `jupyter-book build .`).

## Deploy na Vercel

1. Suba o repositório para o **GitHub** (`git push`).
2. Na **Vercel**: *Add New… → Project → Import* o repositório.
3. Configure **Root Directory = `web`** (o projeto Next vive em `web/`).
4. Framework: **Next.js** (autodetectado). Build command/Output: padrão.
5. Deploy.

Alternativa por CLI (na pasta `web/`): `npx vercel` (login) → `npx vercel --prod`.

> O deploy exige a sua conta (Vercel + GitHub) — não é possível automatizar por aqui.

## Estrutura

| Caminho | O quê |
|---|---|
| `app/` | Páginas (App Router): Home, `trilha`, `modulo/[slug]`, `aula/[...slug]`, `painel`, `diario` |
| `components/` | `Nav`, `Flashcards` (virar), `Mermaid` (render client) |
| `src/lib/` | `preprocess-myst.mjs`, `remark-curso.mjs` (reaproveitados) |
| `scripts/sync-conteudo.mjs` | Compila o conteúdo do curso → `src/data/curso.json` |
| `app/globals.css` | Design system (tokens, prosa, admonitions, dropdowns, flashcards) |
| `public/lite/` | JupyterLite (gerado; não versionado) |
