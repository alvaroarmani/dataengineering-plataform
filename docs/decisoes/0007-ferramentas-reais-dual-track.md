# ADR 0007 — Dual-track com ferramentas reais (elevação para nível profissional)

- **Status:** ✅ Aceito (2026-08-24)
- **Contexto relacionado:** [ADR 0002 (pytest)](0002-correcao-pytest.md), [ADR 0004 (local-first + BigQuery)](0004-local-first-bigquery.md)

## Contexto

Auditoria honesta em 2026-08-24: o construído (M1–M6) tem boa qualidade, mas **tudo roda no
navegador (DuckDB/Pyodide)** e nenhuma ferramenta real é exercitada — a bancada Docker existe
mas fica ociosa, e o módulo "BigQuery" roda DuckDB simulado. Para o objetivo declarado do
usuário ("sair criando DW comercial e pipelines empresariais", stacks Python/dbt/Airflow/
Docker/cloud), isso é insuficiente: falta a metade praticante do curso e a prática com
ferramentas de mercado.

## Decisão

Adotar um **dual-track de prática**:

- **Track browser (fundamentos, M1–M5):** mantém JupyterLite + DuckDB/pandas. Zero-install,
  ótimo para conceitos de Python/SQL/modelagem. Correção por `verificar()`/`pytest`.
- **Track real (ferramentas, M6+):** roda na **bancada Docker** (`ambiente/docker-compose.yml`
  com profiles `dbt`/`airflow`/`spark`, além de Postgres/MinIO) e no **BigQuery free-tier**,
  com **datasets reais** (`datasets/manifest.yaml`). Correção automática de verdade:
  `pytest` contra Postgres (fixture `pg`), `dbt build && dbt test`, `airflow dags test`,
  `docker compose up --wait` + healthcheck. Fora da bancada, os testes fazem **skip**.

Complementos: **≥2 exercícios por unidade + drill sets** (fluência); **rótulos "Onde roda"
honestos**; ordem de construção **espinha primeiro** (M6→M7→M8→M9→M10).

## Consequências

- **Prós:** prática de mercado real e auto-corrigível; a bancada passa a ser usada de fato;
  o mesmo harness alimenta o CI (M13/DataOps); mantém a acessibilidade do track browser para
  fundamentos.
- **Contras:** o track real exige o aluno rodar Docker localmente (não é mais zero-install);
  mais esforço de autoria e de verificação (subir a bancada). Mitigação: skip fora da bancada,
  imagens pinadas, profiles para subir só o necessário.
- **Impacto no padrão:** `.claude/skills/autoria-modulo/SKILL.md` (dual-track + grading real +
  fluência), `templates/template-exercicio-ferramenta/` (novo), `scripts/verificar-conteudo.py`
  (avisos estruturais de fluência/track real). Retrofit de M4–M6 planejado.

Plano completo: seção "ELEVAÇÃO PARA NÍVEL PROFISSIONAL" em
`.claude/plans/estou-querendo-migrar-para-elegant-taco.md`.
