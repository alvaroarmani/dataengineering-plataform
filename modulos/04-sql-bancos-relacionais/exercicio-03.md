# Exercício 03 — Subqueries e CTEs (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Duas queries em etapas sobre a tabela `pedidos(id, estado, categoria, valor, cliente_id)`.

## Tarefas
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py):

- **`CONSULTA_A`** (subquery) — pedidos com `valor` **acima da média geral** de `valor`,
  retornando `id` e `valor`, ordenados por `valor` desc.
- **`CONSULTA_B`** (CTE) — clientes cujo **total gasto** é **maior que a média dos totais**,
  retornando `cliente_id` e `total`, ordenados por `total` desc.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — CONSULTA_A
`WHERE valor > (SELECT AVG(valor) FROM pedidos)`.
:::
:::{dropdown} Dica 2 — CONSULTA_B
Crie uma CTE com o total por cliente e compare com `(SELECT AVG(total) FROM cte)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT id, valor FROM pedidos
WHERE valor > (SELECT AVG(valor) FROM pedidos)
ORDER BY valor DESC;

-- CONSULTA_B
WITH t AS (SELECT cliente_id, SUM(valor) AS total FROM pedidos GROUP BY cliente_id)
SELECT cliente_id, total FROM t
WHERE total > (SELECT AVG(total) FROM t)
ORDER BY total DESC;
```
Em A, a subquery escalar calcula a média uma vez e a consulta externa filtra por ela. Em B,
a CTE `t` nomeia o "total por cliente" e a subquery compara cada total com a média dos totais
— duas etapas, legíveis de cima para baixo.
:::

---
**Revisado em:** 2026-08-22
