# Exercício 03 — Um mart com ref() (TRACK REAL · dbt + Postgres)

**Onde roda:** 🐳 Bancada Docker (dbt real). Sem bancada? Faça o [Exercício 04](exercicio-04.md)
(mesma lógica, no navegador).

O projeto em [`exercicio-03/projeto_dbt/`](exercicio-03/projeto_dbt/) já traz os **staging
models prontos** (`stg_itens`, `stg_produtos`). Você completa o **mart**.

## Tarefa
Complete [`models/fct_receita_categoria.sql`](exercicio-03/projeto_dbt/models/fct_receita_categoria.sql):
junte `{{ ref('stg_itens') }}` e `{{ ref('stg_produtos') }}` por `produto_id` e some `price`
por `categoria`. Colunas: `categoria`, `receita`. Item de produto que não está no cadastro
**não pode sumir**: ele entra na categoria `'Desconhecido'`. O dbt grava tudo no schema `m7_ex03`.

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

> **Armadilhas nos testes:** dois produtos da mesma categoria (a receita soma os dois) e um item de produto fora do cadastro. O grader reconcilia o total do mart com o total dos itens: um `INNER JOIN` derruba o órfão e a conta não fecha. Também confere que o mart é `table` e lê os staging com `ref()`.

## Dicas progressivas
:::{dropdown} Dica 1 — encadeie com ref()
O mart lê **models**, não seeds: `from {{ ref('stg_itens') }} i ... {{ ref('stg_produtos') }} p`, ligados por `produto_id`.
:::
:::{dropdown} Dica 2 — a agregação
Qual tabela manda no grão? Os **itens** (é deles a receita). Por isso o join parte dos itens e
não pode descartar item sem produto: `left join`, não `join`.
:::
:::{dropdown} Dica 3 — quase lá
`select coalesce(p.categoria, 'Desconhecido') as categoria, sum(i.price) as receita
from {{ ref('stg_itens') }} i left join {{ ref('stg_produtos') }} p on i.produto_id = p.produto_id group by 1`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
{{ config(materialized='table') }}

select
    coalesce(p.categoria, 'Desconhecido') as categoria,
    sum(i.price)                          as receita
from {{ ref('stg_itens') }} i
left join {{ ref('stg_produtos') }} p on i.produto_id = p.produto_id   -- LEFT: nada some
group by 1
```
Repare: o mart lê **outros models** (`ref`), não a fonte crua — é isso que constrói o DAG
(`stg_* → fct_*`) e o lineage. O `left join` com `coalesce` garante que o total do mart
reconcilia com o total dos itens: receita de produto fora do cadastro aparece como
`'Desconhecido'` em vez de sumir sem aviso. Marts como `table` porque dashboards os leem muitas vezes.
:::

---
**Revisado em:** 2026-10-21
