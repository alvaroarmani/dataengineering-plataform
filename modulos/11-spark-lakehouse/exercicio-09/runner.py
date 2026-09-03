"""Runner do Exercício 09 (M11) — executa a solução do aluno no Spark e imprime o resultado.

Rodado pelo grader via spark-submit na bancada. Não edite este arquivo.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pyspark.sql import SparkSession  # noqa: E402
from solucao import resumo_por_categoria  # noqa: E402

spark = SparkSession.builder.appName("grader-m11-ex09").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

dados = [("A", 10, 2), ("B", 5, 1), ("A", 3, 4), ("C", 20, 1), ("B", 8, 2)]
df = spark.createDataFrame(dados, ["categoria", "preco", "qtd"])

rows = resumo_por_categoria(df).collect()
out = [[r["categoria"], int(r["total_receita"]), int(r["n_itens"])] for r in rows]
print("RESULT_JSON=" + json.dumps(out))

spark.stop()
