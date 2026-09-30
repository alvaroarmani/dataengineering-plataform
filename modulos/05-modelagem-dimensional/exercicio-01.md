# Exercício 01 — Consultando um star schema (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Duas queries sobre um esquema estrela: `fato_vendas` + `dim_cliente` + `dim_produto`.

## Tabelas
- `fato_vendas(venda_id, cliente_id, produto_id, quantidade, valor)`
- `dim_cliente(cliente_id, nome, cidade)` · `dim_produto(produto_id, categoria)`

## Tarefas
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py):

- **`CONSULTA_A`** — **receita por categoria** (colunas `categoria`, `receita`), desc. Junte o fato com `dim_produto`.
- **`CONSULTA_B`** — **receita por cliente** (colunas `nome`, `receita`), desc. Junte o fato com `dim_cliente`.

```bash
cd modulos/05-modelagem-dimensional/exercicio-01
pytest -q
```

> **Armadilhas nos testes:** além da base do enunciado, as mesmas queries rodam numa base com casos de borda. Venda de produto AUSENTE da dimensão (FK órfã: entra como 'Desconhecido', a receita não some) e cliente HOMÔNIMO (outra 'ana').

## Dicas progressivas
:::{dropdown} Dica 1 — o padrão do star
`FROM fato_vendas f JOIN dim_X d ON f.X_id = d.X_id GROUP BY <atributo> ORDER BY receita DESC`.
:::
:::{dropdown} Dica 2 — a métrica
A receita é `SUM(f.valor)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT COALESCE(p.categoria, 'Desconhecido') AS categoria, SUM(f.valor) AS receita
FROM fato_vendas f LEFT JOIN dim_produto p ON f.produto_id = p.produto_id   -- LEFT: não perde venda
GROUP BY p.categoria ORDER BY receita DESC;

-- CONSULTA_B
SELECT c.nome, SUM(f.valor) AS receita
FROM fato_vendas f JOIN dim_cliente c ON f.cliente_id = c.cliente_id
GROUP BY c.cliente_id, c.nome ORDER BY receita DESC;
```
Repare no padrão: o **fato** carrega a métrica (`valor`) e as **chaves**; cada **dimensão**
traz o atributo descritivo pelo qual você agrupa (categoria, nome). Analisar um star é sempre
"junte o fato com as dimensões que interessam e agregue".

**As armadilhas:** o `LEFT JOIN` + `COALESCE(..., 'Desconhecido')` garante que uma venda com produto ausente da dimensão **não suma** do total — um `JOIN` comum a descartaria em silêncio (é a mesma lição do exercício 11, com dados reais). E agrupar por `cliente_id, nome` evita somar duas pessoas diferentes que se chamam 'ana'.
:::

---
**Revisado em:** 2026-09-30
