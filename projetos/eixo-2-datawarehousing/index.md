# Projeto Integrador — Eixo 2 (Data Warehousing e Modelagem)

> **Star schema + dbt** sobre um dataset real. O coração do futuro TCC.

## Objetivo
Modelar dimensionalmente o dataset Olist e implementar as transformações com **dbt**
(camadas staging → marts), com testes e documentação/lineage.

## Requisitos
1. Diagrama do **star schema** (1 fato + 3+ dimensões), com definição de **grão**.
2. Projeto **dbt** com `sources`, modelos `staging` e `marts`.
3. **Testes dbt** (`unique`, `not_null`, `relationships`) e `dbt docs`.
4. Ao menos uma dimensão com **SCD Tipo 2**.
5. Destino: Postgres local **ou** BigQuery.

## Entregáveis
- Repositório GitHub com o projeto dbt + diagrama + README.

## Rubrica
Ver [rubrica genérica](../../ppc/metodologia-e-avaliacao.md), com peso extra em **modelagem**.

---
**Revisado em:** 2026-08-20
