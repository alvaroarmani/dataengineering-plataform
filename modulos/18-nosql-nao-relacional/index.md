# Módulo 18 — Bancos NoSQL e Não-Relacionais

> Quando a tabela não basta: documento, key-value, wide-column e série temporal — e como
> escolher o banco certo para cada padrão de acesso.

## Identificação
- **Eixo:** 1 — Fundamentos
- **Carga horária:** 25h
- **Pré-requisitos:** M04 (SQL e Bancos Relacionais)
- **Onde roda:** 🟢 Browser (exercícios de lógica) + 🐳 Bancada Docker (MongoDB/Redis — profile `nosql`)

## Ementa
Modelos de dados não-relacionais e seus trade-offs. Quando (e por quê) usar NoSQL: escala horizontal,
flexibilidade de esquema e padrões de acesso. As famílias: **documento** (MongoDB), **key-value**
(Redis), **wide-column** (Cassandra), **grafo** (panorama) e **série temporal**. Schema-on-read,
teorema **CAP** e consistência eventual, quóruns, desnormalização e modelagem **pela consulta**.
Persistência poliglota. Modelagem de documento (embutir vs referenciar), agregação, cache com TTL,
partition/clustering keys e downsampling de séries.

## Competências e habilidades
- C16 — escolher e modelar em bancos NoSQL conforme o padrão de acesso e a escala.

## Objetivos de aprendizagem
1. **Escolher** a família NoSQL adequada a um caso de uso.
2. **Modelar** dados em banco de documento (embed vs reference) e usar agregação.
3. **Aplicar** cache com TTL (key-value) e chaves de partição/clustering (wide-column).
4. **Explicar** CAP, consistência eventual e quóruns.

## Plano de aulas (unidades)

**Unidade 1 — Por que NoSQL? Modelos e trade-offs**
1. **Teoria:** [Por que NoSQL? Modelos e trade-offs (CAP)](teoria-01-por-que-nosql-modelos.md)
2. **Exercícios:** [Escolher a família (🟢)](exercicio-01.md) · [Quórum e consistência (🟢)](exercicio-06.md)

**Unidade 2 — Documento (MongoDB) e key-value (Redis)**
1. **Teoria:** [Documento e key-value](teoria-02-documento-keyvalue.md)
2. **Lab:** [MongoDB na bancada — documentos e agregação (🐳)](lab-01-mongodb-na-bancada.md)
3. **Exercícios:** [Agregar por campo (🟢)](exercicio-02.md) · [Expiração de cache / TTL (🟢)](exercicio-03.md)

**Unidade 3 — Wide-column (Cassandra) e série temporal**
1. **Teoria:** [Wide-column e séries temporais](teoria-03-widecolumn-timeseries.md)
2. **Exercícios:** [Chave de partição (🟢)](exercicio-04.md) · [Downsample de série (🟢)](exercicio-05.md)

> **Módulo completo.** O complemento não-relacional do M04 — fecha a base de bancos de dados do curso.

## Metodologia e avaliação
**Maestria:** escolher a família certa para casos dados, modelar uma coleção de documento (embed vs
reference) e rodar uma agregação no lab, e explicar CAP/quórum — conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Quase toda arquitetura real é **poliglota**: SQL + MongoDB/Redis/Cassandra. Saber escolher e modelar a
família certa (e entender CAP/consistência eventual) é esperado de pleno.

## Erros comuns
- Modelar NoSQL como relacional (normalizar, esperar JOIN).
- Usar Redis como fonte da verdade (é cache/efêmero).
- Partition key ruim em Cassandra (hotspots).
- Série temporal sem retenção/downsampling.

## Recursos
Ver [`recursos.md`](recursos.md) (Kleppmann caps. 2/5/6/9; docs de MongoDB/Redis/Cassandra).

---
**Revisado em:** 2026-08-31
