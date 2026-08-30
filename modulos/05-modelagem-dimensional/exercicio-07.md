# Exercício 07 — SCD2: visão atual e point-in-time (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py):
- **`CONSULTA_A`** — visão ATUAL: (cliente_id, cidade) das linhas correntes, ordenado por cliente_id.
- **`CONSULTA_B`** — point-in-time em 01/01/2025: (cliente_id, cidade) vigente, ordenado por cliente_id.

```bash
cd modulos/05-modelagem-dimensional/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
`WHERE corrente`.
:::
:::{dropdown} Dica 2
`WHERE valido_de <= DATE '2025-01-01' AND DATE '2025-01-01' < valido_ate`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT cliente_id, cidade FROM dim_cliente WHERE corrente ORDER BY cliente_id

-- CONSULTA_B
SELECT cliente_id, cidade FROM dim_cliente WHERE valido_de <= DATE '2025-01-01' AND DATE '2025-01-01' < valido_ate ORDER BY cliente_id
```
:::

---
**Revisado em:** 2026-08-29
