# Exercício 09 — Window functions (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py):
- **`CONSULTA_A`** — (id, rn) com ROW_NUMBER por valor desc, ordenado por rn.
- **`CONSULTA_B`** — (id, acum) soma acumulada por ordem de id.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-09
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
`ROW_NUMBER() OVER (ORDER BY valor DESC)`.
:::
:::{dropdown} Dica 2
`SUM(valor) OVER (ORDER BY id)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT id, ROW_NUMBER() OVER (ORDER BY valor DESC) AS rn FROM itens ORDER BY rn

-- CONSULTA_B
SELECT id, SUM(valor) OVER (ORDER BY id) AS acum FROM itens ORDER BY id
```
:::

---
**Revisado em:** 2026-08-29
