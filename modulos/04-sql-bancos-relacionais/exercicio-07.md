# Exercício 07 — JOIN e agregação (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py):
- **`CONSULTA_A`** — receita (SUM valor) por cidade (cidade, receita), desc.
- **`CONSULTA_B`** — nome do cliente de MAIOR gasto (nome, gasto), 1 linha.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
junte pedidos + clientes por cliente_id.
:::
:::{dropdown} Dica 2
GROUP BY nome, ORDER BY gasto DESC LIMIT 1.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT c.cidade, SUM(p.valor) AS receita FROM pedidos p JOIN clientes c ON p.cliente_id=c.id GROUP BY c.cidade ORDER BY receita DESC

-- CONSULTA_B
SELECT c.nome, SUM(p.valor) AS gasto FROM pedidos p JOIN clientes c ON p.cliente_id=c.id GROUP BY c.nome ORDER BY gasto DESC LIMIT 1
```
:::

---
**Revisado em:** 2026-08-29
