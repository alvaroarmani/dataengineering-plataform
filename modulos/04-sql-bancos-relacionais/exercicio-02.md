# Exercício 02 — JOINs (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Duas queries que **cruzam** `pedidos` com `clientes`.

## Tabelas
- `pedidos(id, estado, categoria, valor, cliente_id)` — 15 linhas.
- `clientes(id, nome, cidade)` — inclui um cliente **sem pedidos** (fabio/Curitiba).

## Tarefas
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py):

- **`CONSULTA_A`** — **total gasto por cliente** (colunas `nome` e `total`), ordenado por `total` desc. Use `JOIN` (clientes sem pedidos podem ficar de fora).
- **`CONSULTA_B`** — **receita por cidade** (colunas `cidade` e `receita`), ordenado por `receita` desc.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — juntar
`FROM pedidos p JOIN clientes c ON p.cliente_id = c.id`.
:::
:::{dropdown} Dica 2 — agrupar
`GROUP BY c.nome` (ou `c.cidade`) com `SUM(p.valor)`; depois `ORDER BY ... DESC`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT c.nome, SUM(p.valor) AS total
FROM pedidos p JOIN clientes c ON p.cliente_id = c.id
GROUP BY c.nome ORDER BY total DESC;

-- CONSULTA_B
SELECT c.cidade, SUM(p.valor) AS receita
FROM pedidos p JOIN clientes c ON p.cliente_id = c.id
GROUP BY c.cidade ORDER BY receita DESC;
```
Como usamos `INNER JOIN`, o cliente sem pedidos (fabio) não aparece — o que é aceitável
aqui, pois ele não tem gasto. Se a pergunta fosse "todos os clientes, mesmo sem gastar",
usaríamos `LEFT JOIN` a partir de `clientes`.
:::

---
**Revisado em:** 2026-08-22
