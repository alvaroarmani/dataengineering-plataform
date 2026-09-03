# Módulo 17 — Streaming e Processamento em Tempo Real (Kafka)

> Quando "amanhã de manhã" é tarde demais: ingestão e processamento de dados **contínuos**,
> orientados a eventos, com Apache Kafka.

## Identificação
- **Eixo:** 3 — Pipelines e Orquestração
- **Carga horária:** 30h
- **Pré-requisitos:** M08 (Ingestão/ETL), M09 (Airflow)
- **Onde roda:** 🟢 Browser (exercícios de lógica) + 🐳 Bancada Docker (Kafka real — profile `kafka`)

## Ementa
Processamento de dados em movimento: **batch vs streaming** e arquiteturas orientadas a eventos.
**Apache Kafka** como log distribuído: tópicos, partições, offsets, produtores/consumidores,
*consumer groups*, ordenação e entrega. Semântica de entrega (at-most/at-least/exactly-once) e
idempotência. **Processamento de streams**: tempo de evento vs de processamento, janelas
(*windows*), estado e *watermarks*; panorama de Kafka Streams e Apache Flink. Ligação com CDC,
data lake/lakehouse (M11) e a arquitetura Lambda/Kappa.

## Competências e habilidades
- C15 — projetar e raciocinar sobre pipelines de streaming com Kafka.

## Objetivos de aprendizagem
1. **Decidir** entre batch e streaming a partir dos requisitos (latência, volume).
2. **Explicar** o modelo do Kafka (tópicos/partições/offsets/consumer groups) e suas garantias.
3. **Raciocinar** sobre entrega, ordenação, idempotência e *lag* de consumidor.
4. **Aplicar** janelas e tempo de evento em agregações de stream.

## Plano de aulas (unidades)

**Unidade 1 — Batch vs Streaming e arquiteturas de eventos**
1. **Teoria:** [Batch vs streaming e o modelo de eventos](teoria-01-batch-vs-streaming-eventos.md)
2. **Exercícios:** [Batch ou streaming? (🟢)](exercicio-01.md) · [Roteamento de eventos (🟢)](exercicio-02.md)

**Unidade 2 — Apache Kafka: o log distribuído**
1. **Teoria:** [Kafka: tópicos, partições, offsets e consumer groups](teoria-02-kafka-topicos-particoes.md)
2. **Lab:** [Kafka na bancada — produza e consuma (🐳)](lab-01-kafka-na-bancada.md)
3. **Exercícios:** [Partição de uma chave (🟢)](exercicio-03.md) · [Lag do consumidor (🟢)](exercicio-04.md) · [**Particionamento no Kafka real (🐳 grader)**](exercicio-07.md)

**Unidade 3 — Processamento de streams: tempo, janelas e garantias**
1. **Teoria:** [Tempo de evento, janelas e semântica de entrega](teoria-03-janelas-tempo-exactly-once.md)
2. **Exercícios:** [Janela por tempo de evento (🟢)](exercicio-05.md) · [Exactly-once por dedup (🟢)](exercicio-06.md)

> **Módulo completo.** Fecha a lacuna de tempo real do Eixo 3 — o complemento streaming do batch (M08/M09).

## Metodologia e avaliação
**Maestria:** explicar o modelo do Kafka e as garantias de entrega, produzir/consumir de um tópico
real na bancada (lab), e resolver os exercícios de particionamento, lag e janelas — conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Streaming (Kafka) aparece em quase toda vaga de Data Engineer pleno. Entender partições, consumer
groups, ordenação e entrega — e quando **não** usar streaming — é diferencial real.

## Erros comuns
- Usar streaming onde batch bastava (complexidade sem necessidade).
- Esperar ordem global num tópico com várias partições (a ordem é **por partição**).
- Ignorar idempotência e reprocessar duplicando.
- Confundir tempo de evento com tempo de processamento nas janelas.

## Recursos
Ver [`recursos.md`](recursos.md) (documentação do Kafka; Kleppmann cap. 11).

---
**Revisado em:** 2026-08-31
