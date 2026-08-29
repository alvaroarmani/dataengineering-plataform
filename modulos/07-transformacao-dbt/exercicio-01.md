# Exercício 01 — Seu primeiro model dbt (TRACK REAL · dbt + Postgres)

**Onde roda:** 🐳 Bancada Docker (dbt real sobre Postgres). Sem bancada? Faça o espelho
auto-corrigível no [Exercício 02](exercicio-02.md) (mesma transformação, no navegador).

Um mini-projeto dbt já está montado em
[`exercicio-01/projeto_dbt/`](exercicio-01/projeto_dbt/): um **seed** (`raw_pedidos.csv`), o
**source** declarado e o model de staging **para você completar**.

## Tarefa
Complete o `SELECT` em [`projeto_dbt/models/stg_pedidos.sql`](exercicio-01/projeto_dbt/models/stg_pedidos.sql)
para produzir as colunas: `pedido_id` (integer), `cliente`, `estado` (a `uf` em MAIÚSCULA),
`valor` (numeric a partir de `valor_str`).

### 1) Suba a bancada e rode o dbt
```bash
cd ambiente && cp .env.example .env && docker compose up -d
# build = seed (carrega o CSV) + run (materializa o model) + test (not_null/unique)
docker compose --profile dbt run --rm dbt build \
  --project-dir  modulos/07-transformacao-dbt/exercicio-01/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-01/projeto_dbt
```
✅ *Verde do dbt:* `PASS` em todos os testes (o `unique`/`not_null` de `pedido_id` e `estado`).

### 2) Confira os valores com o pytest (grader)
```bash
pip install psycopg2-binary pytest
pytest -q modulos/07-transformacao-dbt/exercicio-01
```
> O grader confere a transformação (estado em maiúscula, tipos convertidos). Fora da bancada,
> ele faz *skip*.

## Dicas progressivas
:::{dropdown} Dica 1 — o esqueleto
`select cast(id as integer) as pedido_id, cliente, upper(uf) as estado, cast(valor_str as numeric) as valor from {{ source('olist','raw_pedidos') }}`.
:::
:::{dropdown} Dica 2 — por que source()
Referencie a fonte com `{{ source('olist','raw_pedidos') }}` (não `raw_pedidos` direto) para o dbt construir o lineage e testar a origem.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
select
    cast(id as integer)        as pedido_id,
    cliente,
    upper(uf)                  as estado,
    cast(valor_str as numeric) as valor
from {{ source('olist', 'raw_pedidos') }}
```
Um staging model é limpeza 1:1: renomear (`id`→`pedido_id`), converter tipos (`cast`) e
padronizar (`upper`). Nada de regra de negócio — isso fica nos marts (próxima unidade). O
`dbt build` carregou o seed, materializou a view e rodou os testes numa tacada só.
:::

---
**Revisado em:** 2026-08-24
