# Módulo 08 — Ingestão e Integração de Dados (ETL/ELT)

> Trazer dados de fontes variadas para dentro do seu ambiente, de forma confiável.

## Identificação
- **Eixo:** 3 — Pipelines e Orquestração
- **Carga horária:** 30h
- **Pré-requisitos:** M03, M04
- **Onde roda:** Bancada Docker

## Ementa
ETL vs ELT: quando usar cada um. Padrões de ingestão: full load vs incremental, CDC
(Change Data Capture). Ingestão de arquivos, bancos e APIs (paginação, rate limits,
autenticação). Formatos de dados (CSV, JSON, Parquet, Avro) e por que colunar. Introdução a
streaming e mensageria (Kafka) — conceitual e demo.

## Competências e habilidades
- C7 — ingerir/integrar dados (ETL/ELT, APIs, streaming).

## Objetivos de aprendizagem
1. **Escolher** entre full load e carga incremental (e por quê).
2. **Ingerir** dados de uma API real com paginação e controle de estado.
3. **Comparar** formatos e justificar o uso de Parquet.
4. **Explicar** o papel de streaming/Kafka.

## Plano de aulas (unidades)

**Unidade 1 — ETL vs ELT, incremental, CDC e idempotência**
1. **Teoria:** [Ingestão: ETL/ELT, full vs incremental, CDC](teoria-01-etl-elt-incremental-cdc.md)
2. **Lab:** [Ingestão incremental e idempotente (DuckDB)](lab-01-ingestao-incremental.ipynb)
3. **Exercícios:** [Upsert idempotente (🐳 Postgres real)](exercicio-01.md) · [Lógica do incremental (🟢)](exercicio-02.md)

**Unidade 2 — Ingestão de arquivos e bancos**
1. **Teoria:** [Arquivos e bancos: landing zone, COPY, dedup](teoria-02-ingestao-arquivos-bancos.md)
2. **Lab:** [Ingerir um arquivo e deduplicar a reentrega](lab-02-arquivos-dedup.ipynb)
3. **Exercícios:** [Dedup de reentrega (🐳 Postgres real)](exercicio-03.md) · [Dedup em Python (🟢)](exercicio-04.md)

**Unidade 3 — Ingestão de APIs (paginação, rate limit, auth)**
1. **Teoria:** [Ingestão de APIs](teoria-03-ingestao-apis.md)
2. **Lab (🐳 API real):** [Ingerir a API do Banco Central](lab-03-api-banco-central.md)
3. **Exercícios:** [Paginação (🟢)](exercicio-05.md) · [Retry para rate limit (🟢)](exercicio-06.md)

_Próxima unidade (em construção): formatos de dados (Parquet/Avro) e intro a Kafka._

## Metodologia e avaliação
**Maestria:** implementar ingestão incremental de uma API idempotente, conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Ingestão é o "pão com manteiga" de DE; incremental e idempotência são muito cobrados.

## Erros comuns
- Reingerir tudo sempre (ignorar incremental).
- Não tratar paginação/rate limit de APIs.
- Guardar tudo como CSV.

## Recursos
A curar em `recursos.md` (Densmore *Data Pipelines Pocket Reference*).

---
**Revisado em:** 2026-08-20
