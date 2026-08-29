# Recursos — Módulo 07 (Transformação com dbt)

Curadoria de fontes. Todas registradas em [`referencias.yaml`](../../referencias.yaml).

## Documentação oficial (principal)
- **dbt Docs** — <https://docs.getdbt.com/> (projetos, sources, models, materializations, tests, snapshots, docs/lineage).
- **dbt Fundamentals** (curso gratuito oficial) — ótimo complemento prático.

## Livros
- **Reis, J.; Housley, M. — Fundamentals of Data Engineering** (2022), cap. 8: ELT, analytics engineering.
- **Densmore, J. — Data Pipelines Pocket Reference** (2021): transformação e padrões de pipeline.

## Ferramentas na bancada
- Profile `dbt` do `ambiente/docker-compose.yml` (`ghcr.io/dbt-labs/dbt-postgres:1.8.2`).
- Comando padrão: `docker compose --profile dbt run --rm dbt build --project-dir <projeto> --profiles-dir <projeto>`.

---
**Revisado em:** 2026-08-24
