# Flashcards — Módulo 11

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** O que o Spark melhorou vs MapReduce? / **R:** Mantém dividir+tolerar falhas, mas processa em memória e encadeia operações — muito mais rápido em pipelines multi-passo.
- **P:** Driver vs executors? / **R:** Driver coordena e monta o plano; executors processam partições em paralelo.
- **P:** RDD vs DataFrame? / **R:** DataFrame é alto nível (colunas/tipos), otimizado pelo Catalyst — preferido; RDD é baixo nível.
- **P:** Transformação vs ação (lazy)? / **R:** Transformações (select/filter/groupBy) montam o plano (lazy); ações (count/show/write) disparam a execução.
- **P:** Narrow vs wide? / **R:** Narrow (filter/select) não move dados; wide (groupBy/join/distinct/orderBy) causa shuffle.
- **P:** O que é shuffle e por que é caro? / **R:** Redistribuir dados pela rede para juntar chaves (groupBy/join); envolve rede+disco+serialização — o gargalo do Spark.
- **P:** Como reduzir shuffle? / **R:** Filtrar/projetar cedo, broadcast join para tabelas pequenas, evitar orderBy global; AQE ajuda.
- **P:** O que é data skew? / **R:** Chave concentrada faz uma partição gigante travar o job; mitiga com salting/skew join.
- **P:** Data lake vs lakehouse? / **R:** Lake = arquivos baratos crus (sem ACID); lakehouse = lake + camada de tabela (Delta/Iceberg) com ACID, time travel, schema.
- **P:** O que Delta/Iceberg agregam? / **R:** ACID, time travel (versões), schema enforcement/evolution e MERGE/upsert/delete sobre Parquet.

---
**Revisado em:** 2026-08-29
