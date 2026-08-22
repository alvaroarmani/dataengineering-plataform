# Exercício 05 — HAVING e "segundo maior" (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Dois clássicos de entrevista sobre `pedidos(id, estado, categoria, valor, cliente_id)`.

## Tarefas
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py):

- **`CONSULTA_A`** — clientes com **mais de 3 pedidos** (colunas `cliente_id`, `n`), ordenado
  por `n` desc e depois `cliente_id`. Use `GROUP BY` + `HAVING`.
- **`CONSULTA_B`** — o **segundo maior valor distinto** de pedido (coluna `valor`), em uma
  única linha. Dica: `ORDER BY ... DESC LIMIT 1 OFFSET 1` sobre valores distintos.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — CONSULTA_A
`GROUP BY cliente_id HAVING COUNT(*) > 3` — `HAVING` filtra **grupos**, não linhas.
:::
:::{dropdown} Dica 2 — CONSULTA_B
`SELECT DISTINCT valor FROM pedidos ORDER BY valor DESC LIMIT 1 OFFSET 1`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT cliente_id, COUNT(*) AS n
FROM pedidos
GROUP BY cliente_id
HAVING COUNT(*) > 3
ORDER BY n DESC, cliente_id;

-- CONSULTA_B
SELECT DISTINCT valor FROM pedidos
ORDER BY valor DESC
LIMIT 1 OFFSET 1;
```
`HAVING` só existe por causa da ordem lógica: o filtro por `COUNT(*)` acontece **depois** do
`GROUP BY` (o `WHERE` não enxerga agregações). Em B, `DISTINCT` + `OFFSET 1` pula o maior e
pega o segundo — um padrão clássico para "N-ésimo maior".
:::

---
**Revisado em:** 2026-08-22
