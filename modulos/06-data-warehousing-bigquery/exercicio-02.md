# Exercício 02 — Colunar e particionamento (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Duas consultas que aproveitam o padrão de um DW: ler só o necessário e **filtrar pela coluna
de partição** (`ano`).

## Tabela
`fato_vendas(ano, mes, categoria, valor)` — pense nela particionada por `ano`.

## Tarefas
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py):

- **`CONSULTA_A`** — **pruning**: receita por categoria **apenas de 2025** (`WHERE ano = 2025`),
  colunas `(categoria, receita)` com `SUM(valor)`, da maior para a menor.
- **`CONSULTA_B`** — **range de partição**: receita por ano considerando só `ano >= 2024`,
  colunas `(ano, receita)`, ordenado por `ano` crescente.

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — pruning
Filtre pela coluna de partição: `WHERE ano = 2025` antes de agrupar por `categoria`.
:::
:::{dropdown} Dica 2 — range
`WHERE ano >= 2024`, depois `GROUP BY ano ORDER BY ano`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A: só 2025 (o filtro na coluna de partição habilita o pruning)
SELECT categoria, SUM(valor) AS receita
FROM fato_vendas
WHERE ano = 2025
GROUP BY categoria
ORDER BY receita DESC;

-- CONSULTA_B: range de partição (lê só 2024 e 2025)
SELECT ano, SUM(valor) AS receita
FROM fato_vendas
WHERE ano >= 2024
GROUP BY ano
ORDER BY ano;
```
Em um DW particionado por data, esses filtros fazem o motor **pular** as partições fora do
intervalo — menos bytes varridos, consulta mais rápida e mais barata.
:::

---
**Revisado em:** 2026-08-23
