# Exercício 11 — Integridade: detectar duplicatas (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-11/solucao.py`](exercicio-11/solucao.py):
- **`CONSULTA_A`** — pedido_id que aparecem MAIS DE UMA VEZ (pedido_id), ordenado.
- **`CONSULTA_B`** — (total, distintos) = COUNT(*) e COUNT(DISTINCT pedido_id).

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-11
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
`GROUP BY pedido_id HAVING COUNT(*) > 1`.
:::
:::{dropdown} Dica 2
`COUNT(*)` e `COUNT(DISTINCT pedido_id)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT pedido_id FROM pagamentos GROUP BY pedido_id HAVING COUNT(*) > 1 ORDER BY pedido_id

-- CONSULTA_B
SELECT COUNT(*) AS total, COUNT(DISTINCT pedido_id) AS distintos FROM pagamentos
```
:::

---
**Revisado em:** 2026-08-29
