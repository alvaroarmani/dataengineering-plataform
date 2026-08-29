# Exercício 02 — Staging + mart no navegador (espelho do dbt)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Mesma transformação do [Exercício 01](exercicio-01.md) (dbt real), aqui **auto-corrigível no
navegador** — para praticar a lógica de staging→mart sem depender da bancada.

## Tabela
`raw_pedidos(id, cliente, uf, valor_str)` — dados crus (tudo texto), como um `seed`.

## Tarefas
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py):

- **`CONSULTA_A`** (staging) — limpe para `(pedido_id, cliente, estado, valor)`: `id`→integer,
  `uf`→MAIÚSCULA, `valor_str`→double. Ordene por `pedido_id`.
- **`CONSULTA_B`** (mart) — receita por estado (`SUM(valor)`), da maior para a menor.

```bash
cd modulos/07-transformacao-dbt/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — staging
`SELECT CAST(id AS INTEGER) AS pedido_id, cliente, UPPER(uf) AS estado, CAST(valor_str AS DOUBLE) AS valor FROM raw_pedidos ORDER BY pedido_id`.
:::
:::{dropdown} Dica 2 — mart sobre o staging
Use uma CTE com a lógica de staging e agregue por `estado`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A (staging)
SELECT CAST(id AS INTEGER) AS pedido_id, cliente, UPPER(uf) AS estado, CAST(valor_str AS DOUBLE) AS valor
FROM raw_pedidos
ORDER BY pedido_id;

-- CONSULTA_B (mart)
WITH stg AS (
    SELECT UPPER(uf) AS estado, CAST(valor_str AS DOUBLE) AS valor FROM raw_pedidos
)
SELECT estado, SUM(valor) AS receita
FROM stg
GROUP BY estado
ORDER BY receita DESC;
```
No dbt real, `stg` seria um model (`ref('stg_pedidos')`) e o mart faria `from {{ ref('stg_pedidos') }}` —
a mesma ideia de camadas, com lineage e testes.
:::

---
**Revisado em:** 2026-08-24
