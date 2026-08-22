# ADR 0004 — Local-first + BigQuery como DW cloud

- **Status:** Aceito
- **Data:** 2026-08-20

## Contexto

Praticar Engenharia de Dados em nuvem paga (AWS/GCP/Azure) gera custo e fricção para
quem está estudando. Ao mesmo tempo, o mercado exige experiência com um Data Warehouse
cloud de verdade.

## Decisão

Adotar **local-first**: a maior parte da prática roda em Docker (Postgres, DuckDB, MinIO,
Spark, Airflow), sem custo. Para a experiência cloud de DW, usar **BigQuery**, que tem
*tier gratuito* generoso (armazenamento e consultas mensais) suficiente para o curso e o TCC.

## Consequências

- ✅ Custo próximo de zero para estudar; reprodutível offline.
- ✅ Exposição a um DW colunar cloud real (BigQuery) — valorizado no mercado.
- ⚠️ Conceitos de outras nuvens (Redshift/Snowflake/Databricks) entram como teoria + comparação, não prática paga.
- ⚠️ Exige uma conta Google Cloud (free tier) para os módulos 6 e 7 e o TCC.
