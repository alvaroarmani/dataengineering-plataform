# Exercício 06 — Surrogate keys: gerar e usar (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py):
- **`CONSULTA_A`** — dimensão (sk_produto, codigo, categoria) com ROW_NUMBER OVER (ORDER BY codigo).
- **`CONSULTA_B`** — lookup: (venda_id, sk_produto, valor) juntando stg_venda à dimensão pela chave natural, ordenado por venda_id.

```bash
cd modulos/05-modelagem-dimensional/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
`ROW_NUMBER() OVER (ORDER BY codigo)`.
:::
:::{dropdown} Dica 2
gere a dim numa CTE e junte por codigo.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT ROW_NUMBER() OVER (ORDER BY codigo) AS sk_produto, codigo, categoria FROM stg_produto ORDER BY sk_produto

-- CONSULTA_B
WITH dim AS (SELECT ROW_NUMBER() OVER (ORDER BY codigo) AS sk_produto, codigo, categoria FROM stg_produto) SELECT v.venda_id, d.sk_produto, v.valor FROM stg_venda v JOIN dim d ON v.codigo_produto=d.codigo ORDER BY v.venda_id
```
:::

---
**Revisado em:** 2026-08-29
