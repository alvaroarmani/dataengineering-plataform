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

> **Armadilhas nos testes:** além da base do enunciado, as mesmas queries rodam numa base com casos de borda. Cliente HOMÔNIMO (outra 'ana', em Curitiba) e pedido de cliente inexistente (órfão).

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
GROUP BY c.id, c.nome ORDER BY total DESC;   -- id: nomes se repetem

-- CONSULTA_B
SELECT c.cidade, SUM(p.valor) AS receita
FROM pedidos p JOIN clientes c ON p.cliente_id = c.id
GROUP BY c.cidade ORDER BY receita DESC;
```
Como usamos `INNER JOIN`, o cliente sem pedidos (fabio) não aparece — o que é aceitável
aqui, pois ele não tem gasto. Se a pergunta fosse "todos os clientes, mesmo sem gastar",
usaríamos `LEFT JOIN` a partir de `clientes`.

**A armadilha do homônimo:** `GROUP BY c.nome` somaria as duas 'ana' como se fossem uma pessoa. Agrupe pela **chave** (`c.id`) e só exiba o nome. Já o pedido de cliente inexistente fica de fora do `INNER JOIN` — na unidade de integridade (exercício 11) você aprende a **detectar** esses órfãos em vez de ignorá-los.
:::

---
**Revisado em:** 2026-09-30
