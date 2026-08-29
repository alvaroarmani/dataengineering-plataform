# Exercício 03 — Um mart com ref() (TRACK REAL · dbt + Postgres)

**Onde roda:** 🐳 Bancada Docker (dbt real). Sem bancada? Faça o [Exercício 04](exercicio-04.md)
(mesma lógica, no navegador).

O projeto em [`exercicio-03/projeto_dbt/`](exercicio-03/projeto_dbt/) já traz os **staging
models prontos** (`stg_itens`, `stg_produtos`). Você completa o **mart**.

## Tarefa
Complete [`models/fct_receita_categoria.sql`](exercicio-03/projeto_dbt/models/fct_receita_categoria.sql):
junte `{{ ref('stg_itens') }}` e `{{ ref('stg_produtos') }}` por `produto_id` e some `price`
por `categoria`. Colunas: `categoria`, `receita`.

```bash
cd ambiente && docker compose up -d
docker compose --profile dbt run --rm dbt build \
  --project-dir  modulos/07-transformacao-dbt/exercicio-03/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-03/projeto_dbt
# confere os valores:
pip install psycopg2-binary pytest
pytest -q modulos/07-transformacao-dbt/exercicio-03
```
✅ *Verde:* os testes `not_null`/`unique` do dbt passam **e** o pytest confere a agregação.

## Dicas progressivas
:::{dropdown} Dica 1 — encadeie com ref()
`from {{ ref('stg_itens') }} i join {{ ref('stg_produtos') }} p on i.produto_id = p.produto_id`.
:::
:::{dropdown} Dica 2 — a agregação
`select p.categoria, sum(i.price) as receita ... group by p.categoria`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
{{ config(materialized='table') }}

select
    p.categoria,
    sum(i.price) as receita
from {{ ref('stg_itens') }} i
join {{ ref('stg_produtos') }} p on i.produto_id = p.produto_id
group by p.categoria
```
Repare: o mart lê **outros models** (`ref`), não a fonte crua — é isso que constrói o DAG
(`stg_* → fct_*`) e o lineage. Marts como `table` porque dashboards os leem muitas vezes.
:::

---
**Revisado em:** 2026-08-24
