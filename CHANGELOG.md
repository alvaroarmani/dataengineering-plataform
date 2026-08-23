# Changelog

Histórico de entregas do curso, por fase. Formato inspirado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## [Fase 1] — Esqueleto da plataforma — 2026-08-20

### Adicionado
- Scaffold do Jupyter Book (`_config.yml`, `_toc.yml`, `requirements.txt`, `intro.md`).
- Documentação viva: `ARCHITECTURE.md`, `CONTRIBUTING.md`, ADRs em `docs/decisoes/`.
- PPC completo (9 páginas) no padrão de especialização, com framing honesto.
- 16 módulos com ementa (`index.md`) e recursos curados.
- Método de aprendizado, plano de estudos, tracker de progresso e diário.
- Camada de engajamento: dashboard/mapa vivo, streak, badges, `progresso.json`.
- Bancada Docker (`ambiente/`), catálogo de datasets, especificação do TCC.
- Templates reutilizáveis e a skill de projeto `autoria-modulo`.
- Unidade-referência do Módulo 1 (teoria + lab interativo + exercício `pytest`).

## [Fase 1.1] — Plataforma interativa — 2026-08-20

### Adicionado
- **JupyterLite** integrado (`jupyterlite_sphinx`): notebooks do curso rodam no navegador; botão "▶ Rodar no navegador" no Lab 01, com instalação sob demanda do `duckdb`.
- **Visual de plataforma:** home com cards (sphinx-design), CSS de LMS, barra de progresso no dashboard.
- **Guia de fluxo de autoria** (editar no JupyterLab Docker → salva no arquivo → commit → CI rebuilda) em `CONTRIBUTING.md` e `ARCHITECTURE.md`.

### Alterado
- **Teoria do Módulo 1 expandida:** papel do eng. de dados (hierarquia de necessidades), correntes de fundo do ciclo de vida, colunar/formatos (CSV×Parquet), ETL→ELT, medalhão/Data Mesh, idempotência, boxes de referência com citação, quiz e Q&A de entrevista ampliados; flashcards atualizados.

## [Fase 1.2] — Padrão de conteúdo referenciado — 2026-08-20

### Adicionado
- **`referencias.yaml`** — registro canônico de fontes (livros, papers/artigos abertos, docs oficiais) com chaves.
- **`scripts/verificar-conteudo.py`** — linter de conteúdo: régua por tipo (`conceitual`/`pratico`/`ferramenta`), exige seções/Referências/`Revisado em`, **rejeita citação fora do registro** e faz link-check (`--check-links`, não-bloqueante). Rodando no CI antes do build.
- **`arquitetura-do-curso.md`** — big picture evolutivo (diagrama mestre + mapa eixo→peça).
- **Enriquecimentos de referência no M1:** box "🏭 Do mundo real" (Beauchemin, fonte aberta) e bloco "Perguntas essenciais" (backward design).

### Alterado
- `templates/template-teoria.md` e `template-modulo.md` elevados (tipo, boxes de referência, chaves de citação, perguntas essenciais).
- `.claude/skills/autoria-modulo/SKILL.md` e `CONTRIBUTING.md` — política de referências + registro + Definition of Done com "linter verde".
- M1 marcado como `tipo: conceitual`, referências com chaves do registro.

## [Fase 1.3] — Plataforma de estudos (UI/UX) — 2026-08-21

### Adicionado
- **Mockups (design canvas):** 6 telas — Home, Trilha, Módulo, Aula (split-pane), Exercício, Painel — blend DataCamp/Coursera/Alura.
- **ADR 0005:** plataforma de estudos em **Astro** (frontend bespoke estático), reusando conteúdo + JupyterLite.
- **Casca (PoC) em `plataforma/` (Astro):** design system com **tema claro/escuro**, `Base.astro`, `Nav.astro`, página **Home** (`index.astro`) e **Aula split-pane** (`aula.astro`) com **JupyterLite embarcado** via iframe; responsivo (stack no mobile).
- Ajustes: `plataforma/**` e `node_modules/**` excluídos do build do Jupyter Book; `.gitignore` para node_modules/dist/lite.

## [Fase 1.4] — Plataforma: pipeline de conteúdo — 2026-08-21

### Adicionado
- **Pipeline de conteúdo (Astro):** `scripts/sync-conteudo.mjs` lê `modulos/**` + `progresso.json`, transforma diretivas MyST e gera a coleção `src/content/aulas/` + `src/data/curso.json`.
- **Render nativo** das diretivas via `remark-directive` + `src/lib/remark-curso.mjs` (admonitions e dropdowns estilizados com o design system) e **mermaid** no cliente.
- **Páginas dinâmicas:** Trilha (16 módulos), Módulo (`/modulo/[slug]`) e Aula (`/aula/[...]`) geradas do conteúdo; labs abrem o JupyterLite embarcado.
- **Painel** e **Diário** construídos (streak real, diário com localStorage + "copiar tudo"); navegação unificada.
- ADR 0005 (plataforma em Astro). Conteúdo novo do curso passa a aparecer sozinho após `npm run sync`.

## [Fase 2 — Eixo 2] — em andamento

- **Módulo 5 — Modelagem Dimensional (unidade 1/4):** fatos, dimensões e **grão**, star schema vs snowflake, os 4 passos de Kimball. Teoria conceitual referenciada (Kimball/Reis/Kleppmann) + lab de **star schema no DuckDB** + exercício com 2 queries (fato+dimensões) validado.

## [Fase 1.6] — Migração Next.js + projeto integrador + docs — 2026-08-22

### Adicionado
- **Repositório git dedicado** em `dataengineering/` (antes a raiz era a home, sem commits — risco de privacidade). Baseline no `main`; migração na branch **`plataforma-nextjs`**.
- **Plataforma Next.js** (`web/`, App Router, nosso CSS) reaproveitando conteúdo + pipeline + JupyterLite; render via `react-markdown` + `remark-directive`/`remark-curso`; flashcards e mermaid em React. **Build verificado: 71 páginas estáticas.** Alvo Vercel. (ADR 0006.)
- **Projeto integrador do Eixo 1** (`projetos/eixo-1-fundamentos/`): enunciado + rubrica + **starter** (dados sujos, `ingest/transform/load`, `main.py`, `consultas.sql`, testes `pytest`) — junta Git+Python+SQL num entregável de portfólio. Transformação validada.

### Alterado
- **Documentação viva atualizada:** `ARCHITECTURE.md` (plataforma Next + tabela de stack), `README.md` (estado atual, dois front-ends, como rodar), `docs/decisoes/` (ADR 0006). `web/**` e `**/starter/**` excluídos do build do Jupyter Book.

## [Fase 1.5] — Flashcards interativos + leitura mais leve — 2026-08-22

### Adicionado
- **Flashcards de virar (modo estudo)** na plataforma: `Flashcards.astro` — 1 card por vez, clique/Enter vira, anterior/próximo, contador e barra de progresso (parse dos pares P/R do `flashcards.md`).
- **Polish visual de leitura:** parágrafo-lead, respiro entre blocos, títulos com marcador, e a variante de callout **"✨ Em resumo"** (takeaway).

### Alterado
- **Tom "médio"** nas 5 teorias (M1, M2, M3×3): emojis pontuais nos títulos de seção (🎯 💡 🔎 ⚠️ 💼 🧠 🎤 🚀 📚) + caixa "✨ Em resumo" antes do quiz.
- **Template** de teoria e **skill `autoria-modulo`** atualizados com o tom e a **barra de profundidade** (≥2 exercícios/unidade e datasets reais a partir do M4). Linter segue verde (emojis não quebram as seções).

## [branch plataforma-nextjs] — Migração para Next.js + Vercel — 2026-08-22

### Adicionado
- **Repositório git dedicado** em `dataengineering/` (a raiz antes apontava para a home, sem commits) + baseline Astro no `main`.
- **App Next.js (App Router) em `web/`** com paridade: Home, Trilha, Módulo, Aula (conteúdo + lab + flashcards de virar), Painel, Diário, tema claro/escuro, JupyterLite embarcado.
- **Pipeline** que **compila Markdown → HTML no build** (`web/scripts/sync-conteudo.mjs`, reaproveitando `preprocess-myst` + `remark-curso`); mermaid no cliente.
- ADR 0006 (Next.js + Vercel) e `web/README.md` com passo a passo de deploy.

### Notas
- Conteúdo do curso continua em `modulos/**` (fonte única) — o sync propaga para o Next.
- Deploy na Vercel exige a conta do usuário (Vercel/GitHub).

## [Fase 2 — em andamento] — Eixo 1 (conteúdo)

### Adicionado
- **Módulo 2 — Linux, Git e Ambiente** completo: teoria (terminal, Git, containers) conforme o padrão, lab da bancada Docker + primeiro commit, exercício `pytest` (semântica de `.gitignore`, validado nos dois sentidos), recursos e flashcards. Fontes novas no registro: `chacon2014` (Pro Git), `mit-missing-semester`, `docs-git`.

- **Módulo 3 — Python (unidades 1–2 de ~6):**
  - U1 — estruturas (list/dict/set/tuple, comprehensions): teoria + lab no navegador + exercício `pytest` (top categorias). Fonte: `sweigart-atbs`.
  - U2 — funções, POO e módulos: teoria (funções puras, first-class, classes, dataclasses, módulos) + lab (compor passos + classe) + exercício `pytest` (classe `Pipeline`, validado).
  - U3 — erros, logging e type hints: teoria (try/except específico, quarentena, logging, hints) + lab (quarentena + logging) + exercício `pytest` (`converter_valores`, validado).
  - U4 — pandas: teoria (Series/DataFrame, loc/iloc, máscaras, groupby, merge, NaN) + lab interativo + exercício `pytest` (`receita_por_categoria`, validado).
  - U5 — APIs e formatos (Parquet): teoria (REST/JSON, paginação, rate limit, auth, incremental, CSV×Parquet) + lab (JSON→DataFrame) + exercício `pytest` (`achatar_pedidos`, validado).
  - U6 — testes com pytest e boas práticas: teoria (assert, parametrize, fixtures, casos de borda, estrutura de projeto) + lab (mentalidade de testes) + exercício `pytest` (`validar_registro`, validado). **M3 completo (6 unidades).**
  - Tudo aparece automaticamente nas plataformas (Astro no main / Next na branch) via o pipeline de conteúdo.

- **Módulo 4 — SQL COMPLETO (6 unidades):** modelo relacional + SELECT · JOINs e agregações · subqueries e CTEs · window functions · índices/EXPLAIN e performance · transações/ACID/NoSQL. Cada unidade com teoria referenciada, **lab SQL interativo no navegador (DuckDB)** e exercícios corrigidos por `pytest` via DuckDB (2 queries/unidade nas unidades 1–5; lab de transações no ROLLBACK/COMMIT na 6). Fonte nova: `docs-pytest`.

### Progresso do Eixo 1 — CONCLUÍDO (conteúdo)
- ✅ M1 (Fundamentos) · ✅ M2 (Linux/Git/Docker) · ✅ M3 (Python, 6u) · ✅ M4 (SQL, 6u). Falta só o **projeto integrador do Eixo 1**.

### Pendente do Eixo 1
- Módulo 3: demais unidades (funções/POO, erros/typing, pandas, APIs/Parquet, testes).
- Módulo 4 (SQL) + projeto integrador do Eixo 1.
- Enriquecimentos progressivos: cheat sheets, banco de questões + simulado, troubleshooting.
- Plataforma: portar Trilha/Módulo + pipeline de conteúdo Markdown → Astro.
