# Exercício 01 — Seu primeiro model dbt (TRACK REAL · dbt + Postgres)

**Onde roda:** 🐳 Bancada Docker (dbt real sobre Postgres). Sem bancada? Faça o espelho
auto-corrigível no [Exercício 02](exercicio-02.md) (mesma transformação, no navegador).

Um mini-projeto dbt já está montado em
[`exercicio-01/projeto_dbt/`](exercicio-01/projeto_dbt/): um **seed** (`raw_pedidos.csv`), o
**source** declarado e o model de staging **para você completar**.

## Tarefa
Complete o `SELECT` em [`projeto_dbt/models/stg_pedidos.sql`](exercicio-01/projeto_dbt/models/stg_pedidos.sql)
para produzir as colunas: `pedido_id` (integer), `cliente`, `estado` (a `uf` sem espaços nas
pontas e em MAIÚSCULA), `valor` (numeric a partir de `valor_str`). O dbt grava tudo no schema
`m7_ex01` (definido no `profiles.yml`), separado dos outros exercícios.

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

> **Armadilhas nos testes:** o seed traz uma UF com espaços (`' rj '`): `UPPER` sozinho gera `' RJ '`, que vira um estado à parte em qualquer agregação. O grader também confere os **tipos** das colunas (`integer` e `numeric`) e que nenhuma linha se perdeu.

## Dicas progressivas
:::{dropdown} Dica 1 — o esqueleto
Um staging é limpeza 1:1: cada coluna da fonte vira uma coluna limpa. Comece pelo `select ... from {{ ref('raw_pedidos') }}`
e trate uma coluna de cada vez: renomear, converter o tipo, padronizar o texto.
:::
:::{dropdown} Dica 2 — ref() de um seed (seed × source)
Aqui a fonte crua é um **seed** (o CSV que o dbt carrega), então referenciamos com
`{{ ref('raw_pedidos') }}` — assim o dbt cria a dependência no DAG (o seed carrega **antes** do
model). O `{{ source(...) }}` é para tabelas cruas **externas** (que o dbt não gerencia), declaradas
num `sources.yml`; usá-lo num seed faz o model e o seed rodarem sem ordem e o build falha.
:::
:::{dropdown} Dica 3 — quase lá
`cast(id as integer) as pedido_id`, `cliente`, `upper(trim(uf)) as estado`, `cast(valor_str as numeric) as valor`.
O `trim` vem **antes** do `upper`; a ordem não muda o resultado, mas ler de dentro para fora ajuda.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
select
    cast(id as integer)        as pedido_id,
    cliente,
    upper(trim(uf))            as estado,
    cast(valor_str as numeric) as valor
from {{ ref('raw_pedidos') }}
```
Um staging model é limpeza 1:1: renomear (`id`→`pedido_id`), converter tipos (`cast`) e
padronizar (`trim` + `upper`). Nada de regra de negócio — isso fica nos marts (próxima unidade). O
`dbt build` carregou o seed, materializou a view e rodou os testes numa tacada só.
:::

---
**Revisado em:** 2026-10-21
