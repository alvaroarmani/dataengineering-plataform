# Exercício 12 — Consistência: violações e agregado válido (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-12/solucao.py`](exercicio-12/solucao.py):
- **`CONSULTA_A`** — contas com saldo NEGATIVO (conta), ordenado.
- **`CONSULTA_B`** — soma dos saldos apenas das contas válidas (saldo >= 0) — um número.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-12
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
`WHERE saldo < 0 ORDER BY conta`.
:::
:::{dropdown} Dica 2
`SUM(saldo) WHERE saldo >= 0`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT conta FROM contas WHERE saldo < 0 ORDER BY conta

-- CONSULTA_B
SELECT SUM(saldo) FROM contas WHERE saldo >= 0
```
:::

---
**Revisado em:** 2026-08-29
