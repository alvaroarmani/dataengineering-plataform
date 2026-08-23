# Plataforma de estudos — Next.js

Front-end **oficial** da Especialização em Engenharia de Dados em **Next.js (App Router)**,
para deploy na **Vercel**. Reaproveita o conteúdo do curso (`../modulos`), os plugins remark
e o JupyterLite. Veja o [ADR 0006](../docs/decisoes/0006-nextjs-vercel.md).

## Rodar local

```bash
cd web
npm install
npm run dev      # roda o sync do conteúdo e sobe o Next em http://localhost:3000
```

- `npm run sync` — compila `../modulos/**` → `src/data/curso.json` e copia o JupyterLite para `public/lite`.
- `npm run build` — sync + `next build` (SSG).

> **JupyterLite:** o `public/lite` é **versionado** (gerado pelo Jupyter Book, sem os `.map`)
> para o deploy na Vercel funcionar — a Vercel não roda o Jupyter Book. Para **regenerá-lo**
> após novos labs: `jupyter-book build .` na raiz e copie `_build/html/lite` → `web/public/lite`.

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
| `public/lite/` | JupyterLite (gerado pelo Jupyter Book; **versionado sem os `.map`** para o deploy) |
