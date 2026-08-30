"""Job PySpark de exemplo (M11) — roda na bancada (profile spark).

  docker compose --profile spark run --rm spark spark-submit /work/modulos/11-spark-lakehouse/exemplo/job_spark.py
"""
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("curso-m11").getOrCreate()

dados = [("A", 10, 2), ("B", 5, 1), ("A", 3, 4), ("C", 20, 1)]
df = spark.createDataFrame(dados, ["categoria", "preco", "qtd"])

# transformações (lazy) + ação (show dispara)
(df.withColumn("receita", F.col("preco") * F.col("qtd"))
   .groupBy("categoria")
   .agg(F.sum("receita").alias("total"))
   .orderBy(F.col("total").desc())
   .show())

spark.stop()
