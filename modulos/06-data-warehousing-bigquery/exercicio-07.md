# Exercício 07 — Filtro por partição e agregação (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py):
- **`CONSULTA_A`** — receita por ano SOMENTE da categoria 'A' (ano, receita), ordenado por ano.
- **`CONSULTA_B`** — o mês de MAIOR receita em 2025 (mes, receita), só 1 linha.

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
`WHERE categoria='A'` antes do GROUP BY ano.
:::
:::{dropdown} Dica 2
`WHERE ano=2025 ... ORDER BY receita DESC LIMIT 1`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT ano, SUM(valor) AS receita FROM fato_vendas WHERE categoria='A' GROUP BY ano ORDER BY ano

-- CONSULTA_B
SELECT mes, SUM(valor) AS receita FROM fato_vendas WHERE ano=2025 GROUP BY mes ORDER BY receita DESC LIMIT 1
```
:::

---
**Revisado em:** 2026-08-29
