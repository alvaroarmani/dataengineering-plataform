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

> **Armadilhas nos testes:** além da base do enunciado, as mesmas queries rodam numa base com casos de borda. Staging com o MESMO produto duas vezes (extração duplicada): sem deduplicar, a dimensão ganha 2 linhas para um código e o JOIN do fato DUPLICA vendas (fan-out).

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
SELECT ROW_NUMBER() OVER (ORDER BY codigo) AS sk_produto, codigo, categoria
FROM (SELECT DISTINCT codigo, categoria FROM stg_produto) ORDER BY sk_produto   -- dedup antes da SK

-- CONSULTA_B
WITH dim AS (SELECT ROW_NUMBER() OVER (ORDER BY codigo) AS sk_produto, codigo, categoria
             FROM (SELECT DISTINCT codigo, categoria FROM stg_produto)) SELECT v.venda_id, d.sk_produto, v.valor FROM stg_venda v JOIN dim d ON v.codigo_produto=d.codigo ORDER BY v.venda_id
```

**A armadilha (fan-out):** se a staging traz o mesmo código duas vezes, a dimensão fica com duas linhas para ele e o `JOIN` do fato **duplica** cada venda desse produto — a receita dobra sem erro nenhum. Deduplicar **antes** de gerar a surrogate key (`SELECT DISTINCT`) garante 1 linha por chave natural, a propriedade que todo teste de dimensão (`unique` no dbt, M07) verifica.
:::

---
**Revisado em:** 2026-09-30
