# Exercício 10 — Filtro seletivo (índice ajudaria) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py):
- **`CONSULTA_A`** — contagem por nivel (nivel, n), ordenado por nivel.
- **`CONSULTA_B`** — quantos registros são nivel 'ERROR' (um número).

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-10
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
`GROUP BY nivel ORDER BY nivel`.
:::
:::{dropdown} Dica 2
`WHERE nivel='ERROR'` com COUNT(*).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT nivel, COUNT(*) AS n FROM logs GROUP BY nivel ORDER BY nivel

-- CONSULTA_B
SELECT COUNT(*) FROM logs WHERE nivel='ERROR'
```
:::

---
**Revisado em:** 2026-08-29
