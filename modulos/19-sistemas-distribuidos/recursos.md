# Recursos — Módulo 19 (Sistemas Distribuídos para Dados)

Curadoria de fontes. As obras estão registradas em [`referencias.yaml`](../../referencias.yaml).

## Livro-âncora
- **Kleppmann, M. — Designing Data-Intensive Applications** (2017): **cap. 5** (replicação),
  **cap. 6** (particionamento), **cap. 8** (falhas em sistemas distribuídos), **cap. 9** (consistência
  e consenso). A referência central deste módulo.

## Papers fundadores
- **Dean, J.; Ghemawat, S. — MapReduce: Simplified Data Processing on Large Clusters** (2004):
  computação distribuída tolerante a falhas em hardware comum — o alicerce de Hadoop/Spark.
- **Reis, J.; Housley, M. — Fundamentals of Data Engineering** (2022): sistemas distribuídos no ciclo de vida do dado.

## Documentação e material aberto
- **Raft** — <https://raft.github.io/> (consenso compreensível, com visualização).
- **etcd** — <https://etcd.io/docs/> (consenso como serviço; guarda o estado do Kubernetes, M20).
- **Apache ZooKeeper** — <https://zookeeper.apache.org/> (coordenação distribuída).
- **Apache Cassandra — consistency levels** — <https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html> (quóruns na prática).

## Onde isto aparece no curso
Fundamenta **M11 (Spark)**, **M17 (Kafka)**, **M18 (NoSQL/Cassandra)** e **M20 (Kubernetes/etcd)**.

---
**Revisado em:** 2026-08-31
