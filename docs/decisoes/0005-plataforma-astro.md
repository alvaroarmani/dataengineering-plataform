# ADR 0005 — Plataforma de estudos (UI/UX) em Astro

- **Status:** Aceito
- **Data:** 2026-08-21

## Contexto

O Jupyter Book entrega um ótimo *motor de conteúdo* (teoria + JupyterLite + busca), mas com
**cara de site de documentação**. O usuário quer uma **experiência de plataforma de estudos**
de verdade, inspirada em DataCamp (hands-on split-pane), Coursera/edX (estrutura acadêmica) e
Alura (player limpo, PT-BR). Fizemos **mockups primeiro** (design canvas) para de-riscar; a
direção visual foi aprovada.

## Decisão

Construir um **frontend bespoke estático em Astro** como a plataforma navegável, reusando o
conteúdo Markdown e **embarcando o JupyterLite** (iframe) para os notebooks. Mantém-se
local-first e publicável em **GitHub Pages** (sem backend). Começamos pela **casca**
(Home + página de aula split-pane) como prova de conceito antes de portar todo o conteúdo.

Alternativa considerada e descartada nesta etapa:
- **Skinnar o Jupyter Book** (tema custom): mais rápido, mas teto de "docs site" — não entrega
  a UX de LMS desejada.

## Consequências

- ✅ Controle total de UI/UX (home, trilha, layout de aula split-pane, tema claro/escuro, mobile).
- ✅ Estático/grátis (GitHub Pages); o `referencias.yaml` e o linter de conteúdo seguem válidos (conteúdo é Markdown).
- ⚠️ **Custo de migração:** as diretivas MyST (admonitions, dropdowns, mermaid) precisam ser reimplementadas como componentes/plugins na renderização Markdown do Astro — feito por fase.
- ⚠️ Dois pipelines temporários: o Jupyter Book atual continua servindo o conteúdo até a plataforma Astro assumir; a instância JupyterLite é reaproveitada via iframe.
- ⚠️ O projeto Astro vive em `plataforma/` e é excluído do build do Jupyter Book.
