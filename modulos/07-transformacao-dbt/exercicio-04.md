# Exercício 04 — Consultando o star no navegador (espelho do mart)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Mesma lógica do [Exercício 03](exercicio-03.md) (mart dbt), aqui **auto-corrigível no
navegador** — pratica o join staging + a agregação do mart.

## Tabelas (staging já limpo)
- `stg_itens(item_id, produto_id, price)` · `stg_produtos(produto_id, categoria)`

## Tarefas
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py):

- **`CONSULTA_A`** — receita por categoria (`SUM(price)`), join por `produto_id`, da maior para a menor.
- **`CONSULTA_B`** — ticket médio por categoria (`AVG(price)`), da maior para a menor.

```bash
cd modulos/07-transformacao-dbt/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o join
`FROM stg_itens i JOIN stg_produtos p ON i.produto_id = p.produto_id`.
:::
:::{dropdown} Dica 2 — as métricas
Receita = `SUM(i.price)`; ticket médio = `AVG(i.price)`; agrupe por `p.categoria`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT p.categoria, SUM(i.price) AS receita
FROM stg_itens i JOIN stg_produtos p ON i.produto_id = p.produto_id
GROUP BY p.categoria ORDER BY receita DESC;

-- CONSULTA_B
SELECT p.categoria, AVG(i.price) AS ticket_medio
FROM stg_itens i JOIN stg_produtos p ON i.produto_id = p.produto_id
GROUP BY p.categoria ORDER BY ticket_medio DESC;
```
No dbt real, `stg_itens`/`stg_produtos` seriam `ref()` e este SELECT viraria o model
`fct_receita_categoria` — a mesma consulta, agora versionada, testada e com lineage.
:::

---
**Revisado em:** 2026-08-24
