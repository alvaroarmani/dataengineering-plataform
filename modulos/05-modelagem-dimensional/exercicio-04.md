# Exercício 04 — Analisando o star schema do Olist (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Duas análises de negócio sobre o star schema que você modelou no lab (grão = item de pedido).

## Star schema
- `fato_item_pedido(sk_cliente, sk_produto, price, freight)`
- `dim_cliente(sk_cliente, customer_id, estado)`
- `dim_produto(sk_produto, product_id, categoria)`

## Tarefas
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py):

- **`CONSULTA_A`** — **ticket médio por categoria**: `(categoria, ticket_medio)` com
  `AVG(price)`, do maior para o menor. Junte a fato com `dim_produto`.
- **`CONSULTA_B`** — **receita total por estado**: `(estado, receita)` com
  `SUM(price + freight)`, do maior para o menor. Junte a fato com `dim_cliente`.

```bash
cd modulos/05-modelagem-dimensional/exercicio-04
pytest -q
```

> **Armadilhas nos testes:** além da base do enunciado, as mesmas queries rodam numa base com casos de borda. Item com frete NULL (price + NULL = NULL: sem COALESCE, o preço do item some da receita).

## Dicas progressivas
:::{dropdown} Dica 1 — o padrão do star
`FROM fato_item_pedido f JOIN dim_X d ON f.sk_X = d.sk_X GROUP BY <atributo> ORDER BY <métrica> DESC`.
:::
:::{dropdown} Dica 2 — as métricas
Ticket médio = `AVG(f.price)`; receita total = `SUM(f.price + f.freight)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A: ticket médio por categoria
SELECT dp.categoria, AVG(f.price) AS ticket_medio
FROM fato_item_pedido f
JOIN dim_produto dp ON f.sk_produto = dp.sk_produto
GROUP BY dp.categoria
ORDER BY ticket_medio DESC;

-- CONSULTA_B: receita total (price + freight) por estado
SELECT dc.estado, SUM(f.price + COALESCE(f.freight, 0)) AS receita   -- NULL contamina a soma
FROM fato_item_pedido f
JOIN dim_cliente dc ON f.sk_cliente = dc.sk_cliente
GROUP BY dc.estado
ORDER BY receita DESC;
```
O grão de item permite as duas leituras: `AVG` por produto/categoria e `SUM` por cliente/estado.
É o mesmo modelo respondendo a perguntas diferentes — o valor de um star bem desenhado.

**A armadilha:** `price + NULL` é `NULL`, e o `SUM` ignora `NULL` — então um item sem frete faria o **preço** dele sumir da receita. `COALESCE(f.freight, 0)` deixa explícita a regra de negócio (frete desconhecido conta como zero).
:::

---
**Revisado em:** 2026-09-30
