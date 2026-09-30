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

> **Armadilhas nos testes:** além da base do enunciado, a mesma query roda com um **empate** de receita (o desempate pelo menor `produto_id` precisa estar no `ROW_NUMBER`), uma categoria com **um só** produto e uma venda com valor nulo — perguntas de follow-up clássicas nessa entrevista.

## Dicas progressivas
:::{dropdown} Dica 1 — fale antes de escrever
Como numa entrevista (teoria 02), diga o plano em voz alta: "primeiro agrego a receita por produto, depois rankeio dentro de cada categoria, depois filtro os 2 primeiros". O entrevistador avalia o raciocínio tanto quanto a query.
:::
:::{dropdown} Dica 2 — agregar e rankear
Uma CTE com `SUM(valor)` por `(categoria, produto_id)`; outra com `ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY receita DESC, produto_id ASC)`. O `produto_id` no `ORDER BY` da janela é o desempate — sem ele, empates viram resultados aleatórios.
:::
:::{dropdown} Dica 3 — filtrar e ordenar
Filtre `rn <= 2` na consulta externa (a window roda depois do `WHERE`) e ordene o resultado por `categoria, receita DESC, produto_id`. Categoria com um só produto devolve uma linha só — e está certo.
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
**Revisado em:** 2026-09-30
