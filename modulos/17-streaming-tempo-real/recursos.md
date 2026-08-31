# Recursos — Módulo 17 (Streaming e Tempo Real)

Curadoria de fontes. As obras estão registradas em [`referencias.yaml`](../../referencias.yaml).

## Livro-âncora
- **Kleppmann, M. — Designing Data-Intensive Applications** (2017), **cap. 11 (Stream Processing)**:
  logs particionados, tempo de evento, janelas e semântica de entrega. A referência central deste módulo.
- **Reis, J.; Housley, M. — Fundamentals of Data Engineering** (2022): ingestão e transformação em streaming.
- **Densmore, J. — Data Pipelines Pocket Reference** (2021): padrões de ingestão e brokers.

## Documentação oficial
- **Apache Kafka** — <https://kafka.apache.org/documentation/> (tópicos, partições, consumer groups, entrega).
- **Kafka — Design/Semantics** — <https://kafka.apache.org/documentation/#semantics> (garantias de entrega).
- **Apache Flink** — <https://flink.apache.org/> (tempo de evento, watermarks, exactly-once).
- **Kafka Streams** — <https://kafka.apache.org/documentation/streams/> (processamento com estado sobre Kafka).
- **Spark Structured Streaming** — <https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html> (streaming no Spark, M11).

## Prática
- **Lab deste módulo:** [Kafka na bancada](lab-01-kafka-na-bancada.md) — profile `kafka` do
  [`ambiente/docker-compose.yml`](../../ambiente/docker-compose.yml).

---
**Revisado em:** 2026-08-31
