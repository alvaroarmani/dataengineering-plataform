# Exercício 05 — Consultando um star (quantidade e receita) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py):
- **`CONSULTA_A`** — quantidade total (SUM qtd) por categoria (categoria, qtd), desc.
- **`CONSULTA_B`** — cidade de MAIOR receita (SUM valor) (cidade, receita), 1 linha.

```bash
cd modulos/05-modelagem-dimensional/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
junte fato + dim_produto, GROUP BY categoria.
:::
:::{dropdown} Dica 2
junte fato + dim_cliente, ORDER BY receita DESC LIMIT 1.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT p.categoria, SUM(f.qtd) AS qtd FROM fato_vendas f JOIN dim_produto p ON f.produto_id=p.produto_id GROUP BY p.categoria ORDER BY qtd DESC, p.categoria, p.categoria

-- CONSULTA_B
SELECT c.cidade, SUM(f.valor) AS receita FROM fato_vendas f JOIN dim_cliente c ON f.cliente_id=c.cliente_id GROUP BY c.cidade ORDER BY receita DESC LIMIT 1
```
:::

---
**Revisado em:** 2026-08-29
