# Exercício 08 — Analisando o star do Olist (frete e ticket) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py):
- **`CONSULTA_A`** — frete total (SUM freight) por estado (estado, frete), desc.
- **`CONSULTA_B`** — ticket médio (AVG price) por categoria (categoria, ticket), desc.

```bash
cd modulos/05-modelagem-dimensional/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
junte fato_item + dim_cliente.
:::
:::{dropdown} Dica 2
junte fato_item + dim_produto, AVG(price).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT c.estado, SUM(f.freight) AS frete FROM fato_item f JOIN dim_cliente c ON f.sk_cliente=c.sk_cliente GROUP BY c.estado ORDER BY frete DESC

-- CONSULTA_B
SELECT p.categoria, AVG(f.price) AS ticket FROM fato_item f JOIN dim_produto p ON f.sk_produto=p.sk_produto GROUP BY p.categoria ORDER BY ticket DESC
```
:::

---
**Revisado em:** 2026-08-29
