# Exercício 08 — Subquery e CTE (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py):
- **`CONSULTA_A`** — total por vendedor (vendedor, total), ordenado por total desc e vendedor.
- **`CONSULTA_B`** — vendedores com total ACIMA da média dos totais (vendedor), ordenado por vendedor.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
GROUP BY vendedor.
:::
:::{dropdown} Dica 2
use uma CTE com os totais e compare com (SELECT AVG(tot) FROM cte).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT vendedor, SUM(valor) AS total FROM vendas GROUP BY vendedor ORDER BY total DESC, vendedor

-- CONSULTA_B
WITH t AS (SELECT vendedor, SUM(valor) AS tot FROM vendas GROUP BY vendedor) SELECT vendedor FROM t WHERE tot > (SELECT AVG(tot) FROM t) ORDER BY vendedor
```
:::

---
**Revisado em:** 2026-08-29
