# Exercício 08 — Pruning por intervalo de data (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py):
- **`CONSULTA_A`** — receita por tipo em JANEIRO/2026 (tipo, receita), ordenado por tipo.
- **`CONSULTA_B`** — receita por tipo em FEVEREIRO/2026 (tipo, receita), ordenado por tipo.

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
Filtre `dia >= '2026-01-01' AND dia < '2026-02-01'`.
:::
:::{dropdown} Dica 2
Idem para fevereiro.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT tipo, SUM(valor) AS receita FROM eventos WHERE dia >= DATE '2026-01-01' AND dia < DATE '2026-02-01' GROUP BY tipo ORDER BY tipo

-- CONSULTA_B
SELECT tipo, SUM(valor) AS receita FROM eventos WHERE dia >= DATE '2026-02-01' AND dia < DATE '2026-03-01' GROUP BY tipo ORDER BY tipo
```
:::

---
**Revisado em:** 2026-08-29
