# Exercício 04 — Window functions (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Duas queries com `OVER (...)` sobre `pedidos(id, estado, categoria, valor, cliente_id)`.

## Tarefas
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py):

- **`CONSULTA_A`** — o **pedido de maior valor de cada estado** (colunas `estado`, `id`,
  `valor`), ordenado por `valor` desc. Use `ROW_NUMBER()` numa CTE e filtre a posição 1.
- **`CONSULTA_B`** — a **receita por estado** (colunas `estado`, `receita`) usando uma
  **window function** (`SUM(...) OVER (PARTITION BY estado)`) + `DISTINCT`, ordenado por `receita` desc.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — CONSULTA_A
`WITH r AS (SELECT estado, id, valor, ROW_NUMBER() OVER (PARTITION BY estado ORDER BY valor DESC) rn FROM pedidos) SELECT estado, id, valor FROM r WHERE rn = 1 ORDER BY valor DESC`.
:::
:::{dropdown} Dica 2 — CONSULTA_B
`SELECT DISTINCT estado, SUM(valor) OVER (PARTITION BY estado) AS receita FROM pedidos ORDER BY receita DESC`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
WITH r AS (
    SELECT estado, id, valor,
           ROW_NUMBER() OVER (PARTITION BY estado ORDER BY valor DESC) AS rn
    FROM pedidos
)
SELECT estado, id, valor FROM r WHERE rn = 1 ORDER BY valor DESC;

-- CONSULTA_B
SELECT DISTINCT estado, SUM(valor) OVER (PARTITION BY estado) AS receita
FROM pedidos ORDER BY receita DESC;
```
Em A, `ROW_NUMBER` numera os pedidos dentro de cada estado por valor; filtrar `rn = 1`
(numa consulta externa, pois a window roda depois do WHERE) dá o maior de cada estado. Em B,
a agregação em janela repete a receita do estado em cada linha; `DISTINCT` reduz para uma
linha por estado — sem colapsar via GROUP BY.
:::

---
**Revisado em:** 2026-08-22
