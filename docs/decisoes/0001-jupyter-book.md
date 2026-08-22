# ADR 0001 — Plataforma: Jupyter Book + JupyterLite + Docker

- **Status:** Aceito
- **Data:** 2026-08-20

## Contexto

Queremos uma plataforma de curso com páginas de teoria, notebooks interativos, correção
de atividades e links de vídeo — construída e mantida por uma pessoa, local-first, e
publicável de graça.

## Decisão

Usar **Jupyter Book** (Sphinx/MyST) para gerar um site estático navegável;
**JupyterLite** (Pyodide) para rodar notebooks de fundamentos no navegador sem
instalação; e uma **bancada Docker** para os labs que exigem infraestrutura real
(Postgres, Airflow, dbt, Spark, MinIO). Publicação em **GitHub Pages**.

Alternativas consideradas:
- **App web custom (Next.js/React):** controle total de UX, mas ~10x mais esforço e vira um LMS para manter — distrai do objetivo de aprender.
- **JupyterLab local + nbgrader apenas:** fiel ao dia a dia, mas sem site público navegável.

## Consequências

- ✅ Notebooks são cidadãos de primeira classe; publicação gratuita; baixo custo de manutenção.
- ✅ Fundamentos rodam no browser (fricção quase zero para começar).
- ⚠️ O Pyodide não roda Spark/Postgres/Airflow — por isso a bancada Docker é a *bancada principal* para engenharia real.
- ⚠️ Sem backend: progresso vive em `localStorage` + `progresso.json` versionado.
