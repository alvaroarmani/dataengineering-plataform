# Exercício 06 — SELECT: filtro e agregação (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py):
- **`CONSULTA_A`** — (nome, preco) de 'eletronicos' com preco > 100, ordenado por preco desc.
- **`CONSULTA_B`** — preço médio por categoria (categoria, media), ordenado por categoria.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
`WHERE categoria='eletronicos' AND preco>100 ORDER BY preco DESC`.
:::
:::{dropdown} Dica 2
`GROUP BY categoria ORDER BY categoria`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT nome, preco FROM produtos WHERE categoria='eletronicos' AND preco>100 ORDER BY preco DESC

-- CONSULTA_B
SELECT categoria, AVG(preco) AS media FROM produtos GROUP BY categoria ORDER BY categoria
```
:::

---
**Revisado em:** 2026-08-29
