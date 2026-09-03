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

## Dica
:::{dropdown} Dica
`df.withColumn("receita", F.col("preco") * F.col("qtd")).groupBy("categoria").agg(F.sum("receita").alias("total_receita"), F.count("*").alias("n_itens")).orderBy(F.col("total_receita").desc())`.
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
**Revisado em:** 2026-09-03
