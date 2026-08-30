# Exercício 03 — SQL ao vivo: top N por grupo (com pytest)

**Onde roda:** 🟢 Browser (DuckDB). Simula a prova de **SQL ao vivo** de entrevista.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): preencha **`CONSULTA`** para retornar os
**2 produtos de maior receita em cada categoria**, colunas `(categoria, produto_id, receita)`,
ordenado por `categoria` ASC e `receita` DESC (desempate por `produto_id` ASC).

Tabela: `vendas(produto_id, categoria, valor)`.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
Como numa entrevista, pense em voz alta e resolva em passos: (1) agregue a receita por
`(categoria, produto_id)` numa CTE; (2) rankeie dentro da categoria com
`ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY SUM(valor) DESC, produto_id ASC)`;
(3) filtre `rn <= 2` e ordene o resultado final.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
WITH receita AS (
    SELECT categoria, produto_id, SUM(valor) AS receita
    FROM vendas
    GROUP BY categoria, produto_id
),
ranqueado AS (
    SELECT categoria, produto_id, receita,
           ROW_NUMBER() OVER (
               PARTITION BY categoria
               ORDER BY receita DESC, produto_id ASC
           ) AS rn
    FROM receita
)
SELECT categoria, produto_id, receita
FROM ranqueado
WHERE rn <= 2
ORDER BY categoria ASC, receita DESC, produto_id ASC
```
:::

---
**Revisado em:** 2026-08-30
