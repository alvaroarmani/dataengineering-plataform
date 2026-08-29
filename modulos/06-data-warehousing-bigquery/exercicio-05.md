# Exercício 05 — Consultas cost-aware (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Escreva consultas que leem **só o necessário** — o hábito que mantém as queries baratas no DW.

## Tabela
`fato(ano, mes, categoria, price, descricao)` — pense nela particionada por `ano`. A coluna
`descricao` é "gorda": **não** a selecione.

## Tarefas
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py):

- **`CONSULTA_A`** — receita por categoria em **2025**: `(categoria, receita)` = `SUM(price)`,
  da maior para a menor. Só as colunas necessárias + `WHERE ano = 2025`.
- **`CONSULTA_B`** — o **mês de maior receita** em 2025: `(mes, receita)`, apenas 1 linha.

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — cost-aware
Selecione só `categoria, price` (nunca `descricao` nem `SELECT *`) e filtre `WHERE ano = 2025`.
:::
:::{dropdown} Dica 2 — o maior mês
Agrupe por `mes`, `ORDER BY receita DESC` e `LIMIT 1`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT categoria, SUM(price) AS receita
FROM fato
WHERE ano = 2025
GROUP BY categoria
ORDER BY receita DESC;

-- CONSULTA_B
SELECT mes, SUM(price) AS receita
FROM fato
WHERE ano = 2025
GROUP BY mes
ORDER BY receita DESC
LIMIT 1;
```
Ao ler só `categoria/price/mes` e filtrar `ano`, você varre uma fração dos bytes — o mesmo
resultado por uma fração do custo. `LIMIT 1` aqui serve para pegar o topo (não reduz o custo
da varredura, como visto na teoria).
:::

---
**Revisado em:** 2026-08-24
