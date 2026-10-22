# Exercício 09 — Resumo por categoria em PySpark (TRACK REAL · Spark)

**Onde roda:** 🐳 Bancada Docker (**Spark de verdade**, profile `spark`). Este é o exercício
auto-corrigível que roda no **Spark real** — o grader executa a sua solução via `spark-submit` e
confere o resultado. Sem bancada? Os exercícios 01–08 cobrem a mesma lógica no navegador.

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py), implemente **`resumo_por_categoria(df)`**
usando a API do PySpark. O `df` tem as colunas `(categoria, preco, qtd)`. Retorne, por categoria:
- `total_receita` = soma de `preco * qtd`
- `n_itens` = contagem de linhas

ordenado por `total_receita` **decrescente** (colunas: `categoria, total_receita, n_itens`).

## Como rodar o grader
Suba a bancada e rode o `pytest` (ele chama o `spark-submit` por você):
```bash
cd ambiente && docker compose up -d          # postgres/minio/jupyter
pytest -q modulos/11-spark-lakehouse/exercicio-09
```
> O grader sobe um container Spark sob demanda, roda a sua `resumo_por_categoria` sobre um
> DataFrame de teste e compara o resultado. **Fora da bancada, ele faz *skip*** (não falha).

> **Armadilhas nos testes:** além do resultado no Spark (na bancada), checagens que rodam sem Docker: nenhuma ação (`collect`, `show`, `toPandas`) dentro da função, nenhuma UDF Python e as saídas nomeadas com `alias`.

## Dicas progressivas
:::{dropdown} Dica 1 — pense em SQL primeiro
O resultado é um `SELECT categoria, SUM(preco * qtd) AS total_receita, COUNT(*) AS n_itens ... GROUP BY categoria ORDER BY total_receita DESC`. Traduzir para a API do DataFrame é trocar cada cláusula pelo método equivalente.
:::
:::{dropdown} Dica 2 — os métodos
Coluna derivada: `withColumn("receita", F.col("preco") * F.col("qtd"))`. Agregação: `groupBy("categoria").agg(...)` com `F.sum(...).alias(...)` e `F.count("*").alias(...)`. Ordenação: `orderBy(F.col("total_receita").desc())`.
:::
:::{dropdown} Dica 3 — o detalhe que o grader confere
Os **nomes** das colunas de saída precisam ser exatamente `categoria`, `total_receita` e `n_itens` — use `.alias(...)` em cada agregação. E devolva o DataFrame (não chame `.show()` nem `.collect()` dentro da função).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from pyspark.sql import functions as F

def resumo_por_categoria(df):
    return (
        df.withColumn("receita", F.col("preco") * F.col("qtd"))
          .groupBy("categoria")
          .agg(F.sum("receita").alias("total_receita"),
               F.count("*").alias("n_itens"))
          .orderBy(F.col("total_receita").desc())
    )
```
:::

---
**Revisado em:** 2026-09-30
