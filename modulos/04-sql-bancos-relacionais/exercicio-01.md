# Exercício 01 — Suas primeiras queries (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Você vai **escrever SQL** e o teste roda sua query contra uma tabela `pedidos` real,
conferindo o resultado. São **duas tarefas** (2 queries).

## A tabela `pedidos`
Colunas: `id`, `estado`, `categoria`, `valor`, `cliente_id` — 15 pedidos (SP/RJ/MG).

## Tarefas
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), preencha **duas** strings SQL:

- **`CONSULTA_A`** — os pedidos de **SP** com `valor > 100`, retornando **`id`** e **`valor`**,
  ordenados por **`valor` decrescente**.
- **`CONSULTA_B`** — a **receita por categoria** (colunas **`categoria`** e **`receita`** =
  soma dos valores), ordenada por **`receita` decrescente**.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — CONSULTA_A
`SELECT id, valor FROM pedidos WHERE estado = 'SP' AND valor > 100 ORDER BY valor DESC`.
:::
:::{dropdown} Dica 2 — CONSULTA_B
`GROUP BY categoria` com `SUM(valor) AS receita`, depois `ORDER BY receita DESC`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT id, valor
FROM pedidos
WHERE estado = 'SP' AND valor > 100
ORDER BY valor DESC;

-- CONSULTA_B
SELECT categoria, SUM(valor) AS receita
FROM pedidos
GROUP BY categoria
ORDER BY receita DESC;
```
Repare: o `WHERE` filtra linhas **antes** de qualquer agregação; o `GROUP BY` cria um grupo
por categoria e o `SUM` agrega dentro de cada grupo; o `ORDER BY` no fim organiza a saída.
:::

---
**Revisado em:** 2026-08-22
