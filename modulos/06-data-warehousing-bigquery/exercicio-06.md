# Exercício 06 — Camadas: core e mart (agregações) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py):
- **`CONSULTA_A`** — core: (pedido_id, cliente, estado em MAIÚSCULA, valor) SEM duplicatas, ordenado por pedido_id.
- **`CONSULTA_B`** — mart: nº de clientes DISTINTOS por estado (estado, n), ordenado por estado.

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-06
pytest -q
```

> **Armadilhas nos testes:** além da base do enunciado, as mesmas queries rodam numa base com casos de borda. A mesma cliente em dois estados (conta uma vez em CADA estado) e um cliente com dois pedidos no mesmo estado (conta uma vez só).

## Dicas progressivas
:::{dropdown} Dica 1
`SELECT DISTINCT ... UPPER(estado) ...`.
:::
:::{dropdown} Dica 2
Use uma CTE com o core e `COUNT(DISTINCT cliente)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT DISTINCT pedido_id, cliente, UPPER(estado) AS estado, valor FROM raw_pedidos ORDER BY pedido_id

-- CONSULTA_B
WITH core AS (SELECT DISTINCT pedido_id, cliente, UPPER(estado) AS estado, valor FROM raw_pedidos) SELECT estado, COUNT(DISTINCT cliente) AS n FROM core GROUP BY estado ORDER BY estado
```
:::

---
**Revisado em:** 2026-09-30
