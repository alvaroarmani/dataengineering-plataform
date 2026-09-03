# Recursos — Módulo 11 (Spark + Lakehouse)

Curadoria de fontes. Todas registradas em [`referencias.yaml`](../../referencias.yaml).

## Documentação oficial
- **Apache Spark** — <https://spark.apache.org/docs/latest/> (DataFrame API, tuning, AQE).
- **Delta Lake** / **Apache Iceberg** — formatos de tabela (ACID, time travel).

## Papers e livros
- **Dean & Ghemawat — MapReduce** (2004): o modelo fundador.
- **Armbrust et al. — Delta Lake** (2020): camada ACID sobre object storage.
- **Kleppmann — Designing Data-Intensive Applications**, cap. 10 (batch/distribuído, shuffle).
- **Reis, J.; Housley, M. — Fundamentals of Data Engineering** (2022): escala, lake/lakehouse.

## Ferramentas na bancada
- Profile `spark` (`apache/spark:3.5.3`) + `minio` (object storage S3 local) do `ambiente/docker-compose.yml`.
- Exemplo PySpark: `modulos/11-spark-lakehouse/exemplo/job_spark.py`.
- Rodar: `docker compose --profile spark run --rm spark /opt/spark/bin/spark-submit /work/.../job_spark.py` (Git Bash: `MSYS_NO_PATHCONV=1`).

---
**Revisado em:** 2026-08-29
