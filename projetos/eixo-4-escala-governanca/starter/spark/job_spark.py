"""Trilha real (bancada) — o mesmo processamento em PySpark, gravando Parquet no MinIO (S3).

Rode na bancada com o profile spark (M11). TODO: complete a transformação/agregação em Spark
(espelhando processamento.py) e a escrita particionada no MinIO.
"""
from pyspark.sql import SparkSession, functions as F


def main():
    spark = (
        SparkSession.builder.appName("eixo4-corridas")
        # MinIO (S3A) — ajuste endpoint/credenciais conforme a bancada
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minio")
        .config("spark.hadoop.fs.s3a.secret.key", "minio12345")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .getOrCreate()
    )
    df = spark.read.option("header", True).csv("data/amostra_corridas.csv")
    # TODO: duracao_min, data, filtrar inválidos, agregar por dia
    # TODO: escrever particionado por data em Parquet no MinIO:
    #   agg.write.mode("overwrite").partitionBy("data").parquet("s3a://curso/corridas/")
    spark.stop()


if __name__ == "__main__":
    main()
