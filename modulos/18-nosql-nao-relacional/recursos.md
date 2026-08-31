# Recursos — Módulo 18 (NoSQL e Não-Relacional)

Curadoria de fontes. As obras estão registradas em [`referencias.yaml`](../../referencias.yaml).

## Livro-âncora
- **Kleppmann, M. — Designing Data-Intensive Applications** (2017): **cap. 2** (modelos: relacional,
  documento, grafo), **cap. 5** (replicação), **cap. 6** (particionamento), **cap. 9** (consistência/
  consenso). A referência central deste módulo.
- **Reis, J.; Housley, M. — Fundamentals of Data Engineering** (2022): sistemas de armazenamento NoSQL.
- **Tanimura, C. — SQL for Data Analysis** (2021): o contraponto relacional (M04).

## Documentação oficial das famílias
- **MongoDB (documento)** — <https://www.mongodb.com/docs/> (modelagem, aggregation pipeline, índices).
- **Redis (key-value)** — <https://redis.io/docs/> (estruturas, TTL, padrões de cache).
- **Apache Cassandra (wide-column)** — <https://cassandra.apache.org/doc/> (partition/clustering keys, data modeling).
- **TimescaleDB (série temporal)** — <https://docs.timescale.com/> · **InfluxDB** — <https://docs.influxdata.com/>.
- **Neo4j (grafo)** — <https://neo4j.com/docs/> (nós, arestas, Cypher).

## Prática
- **Lab deste módulo:** [MongoDB na bancada](lab-01-mongodb-na-bancada.md) — profile `nosql`
  (Mongo + Redis) do [`ambiente/docker-compose.yml`](../../ambiente/docker-compose.yml).

---
**Revisado em:** 2026-08-31
