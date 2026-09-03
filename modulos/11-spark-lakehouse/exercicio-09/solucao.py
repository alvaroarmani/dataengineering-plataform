"""Exercício 09 (M11) — Resumo por categoria em PySpark (TRACK REAL · Spark na bancada).

Implemente a transformação usando a API do PySpark. O grader roda de verdade via
`spark-submit` na bancada (profile spark) e confere o resultado. Ver enunciado.
"""
from pyspark.sql import DataFrame, functions as F


def resumo_por_categoria(df: DataFrame) -> DataFrame:
    """df tem as colunas (categoria, preco, qtd). Retorne um DataFrame com, por categoria:
      - total_receita = soma de (preco * qtd)
      - n_itens       = contagem de linhas
    ordenado por total_receita DESC. Colunas de saída: categoria, total_receita, n_itens.
    """
    # SEU CÓDIGO AQUI (use df.withColumn, groupBy, agg, orderBy)
    raise NotImplementedError
