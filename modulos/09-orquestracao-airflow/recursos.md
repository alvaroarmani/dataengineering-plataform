# Recursos — Módulo 09 (Orquestração com Airflow)

Curadoria de fontes. Todas registradas em [`referencias.yaml`](../../referencias.yaml).

## Documentação oficial (principal)
- **Apache Airflow Docs** — <https://airflow.apache.org/docs/> (Core Concepts, DAGs, Operators, Scheduling, Best Practices).
- **Astronomer — Airflow Fundamentals** (trilha gratuita) — ótimo complemento prático.

## Livros
- **Reis, J.; Housley, M. — Fundamentals of Data Engineering** (2022): orquestração como undercurrent.
- **Densmore, J. — Data Pipelines Pocket Reference** (2021): agendamento, dependências, idempotência.

## Ferramentas na bancada
- Profile `airflow` do `ambiente/docker-compose.yml` (`apache/airflow:2.10.3`, LocalExecutor sobre o Postgres).
- DAGs em `modulos/09-orquestracao-airflow/dags/` (montadas em `/opt/airflow/dags`).
- Subir: `docker compose --profile airflow up -d` · UI: <http://localhost:8080>.

---
**Revisado em:** 2026-08-29
