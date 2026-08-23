# ADR 0006 — Migração da plataforma para Next.js + Vercel

- **Status:** ✅ Aceito e concluído — Astro removido em 2026-08-23; Next.js é a plataforma oficial (`web/`). Pendente apenas o deploy na Vercel.
- **Data:** 2026-08-22 (concluído em 2026-08-23)

## Contexto

A plataforma de estudos foi construída em **Astro** (ADR 0005), estática, publicável no
GitHub Pages. O usuário decidiu migrar para **Next.js** com deploy na **Vercel** — pela
familiaridade do ecossistema React/Next, pela integração nativa com a Vercel, e para abrir
caminho a **backend depois** (API routes: progresso sincronizado, login) que o site estático
não oferecia. A migração é feita numa **branch** (`plataforma-nextjs`) para preservar o Astro.

**Achado de segurança:** o repositório git estava com raiz na **home** do usuário
(`C:\Users\alvaro`), sem commits — commitar assim varreria a pasta pessoal. Corrigido com um
**repositório git dedicado** dentro de `dataengineering/`.

## Decisão

- **Front-end:** Next.js (App Router) em `web/`, SSG, com o **nosso CSS** portado (sem
  Tailwind, para preservar o design aprovado). Coexiste com `plataforma/` (Astro) durante a
  transição; o Astro permanece intacto no `main`.
- **Conteúdo reaproveitado:** o Markdown do curso, o pipeline de sync, os plugins remark
  (`remark-directive` + `remark-curso`) e o Jupyter Book (gerador do JupyterLite) são
  reusados. Render de Markdown via `react-markdown` + os mesmos plugins + `rehype-raw`
  (para o `<pre class="mermaid">`).
- **Deploy:** Vercel (Root Directory = `web/`). O deploy em si depende da conta do usuário
  (Vercel/GitHub) — não automatizável por aqui.

## Consequências

- ✅ UI/UX em React/Next (skill de mercado), Vercel-native, porta aberta para backend futuro.
- ✅ Zero retrabalho de conteúdo: mesma fonte `modulos/**` alimenta Astro e Next.
- ✅ Baseline preservado no `main` (Astro) e migração isolada na branch.
- ⚠️ **Dois front-ends** temporariamente (Astro + Next) — decidir aposentar o Astro quando o Next atingir paridade total.
- ⚠️ O Jupyter Book segue como gerador do JupyterLite e como o site de conteúdo "de referência".
- ⚠️ A instância JupyterLite (~70 MB) é copiada para `web/public/lite` (gerada, fora do git).
