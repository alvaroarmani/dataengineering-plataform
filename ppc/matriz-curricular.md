# Matriz Curricular

**16 disciplinas · 5 eixos · ~550 horas** (mínimo MEC para *lato sensu*: 360h).

A sequência respeita pré-requisitos: fundamentos → modelagem/DW → pipelines →
escala/governança → carreira → TCC.

## Eixo 1 — Fundamentos (155h)

| # | Disciplina | CH | Pré-requisitos |
|---|---|---|---|
| M01 | [Fundamentos de Eng. de Dados e Arquitetura](../modulos/01-fundamentos-eng-dados/index.md) | 30h | — |
| M02 | [Linux, Git e Ambiente de Desenvolvimento](../modulos/02-linux-git-ambiente/index.md) | 20h | M01 |
| M03 | [Python para Engenharia de Dados](../modulos/03-python-eng-dados/index.md) | 60h | M02 |
| M04 | [SQL e Bancos de Dados Relacionais](../modulos/04-sql-bancos-relacionais/index.md) | 45h | M02 |

## Eixo 2 — Data Warehousing e Modelagem (110h)

| # | Disciplina | CH | Pré-requisitos |
|---|---|---|---|
| M05 | [Modelagem de Dados e Dimensional (Kimball)](../modulos/05-modelagem-dimensional/index.md) | 40h | M04 |
| M06 | [Data Warehousing: Teoria e Prática + BigQuery](../modulos/06-data-warehousing-bigquery/index.md) | 40h | M05 |
| M07 | [Transformação de Dados com dbt](../modulos/07-transformacao-dbt/index.md) | 30h | M06 |

## Eixo 3 — Pipelines e Orquestração (95h)

| # | Disciplina | CH | Pré-requisitos |
|---|---|---|---|
| M08 | [Ingestão e Integração de Dados (ETL/ELT)](../modulos/08-ingestao-integracao/index.md) | 30h | M03, M04 |
| M09 | [Orquestração de Workflows com Apache Airflow](../modulos/09-orquestracao-airflow/index.md) | 40h | M03, M08 |
| M10 | [Containers e Deploy: Docker avançado](../modulos/10-docker-avancado/index.md) | 25h | M02 |

## Eixo 4 — Escala, Qualidade e Governança (110h)

| # | Disciplina | CH | Pré-requisitos |
|---|---|---|---|
| M11 | [Processamento em Larga Escala (Spark) + Lakehouse](../modulos/11-spark-lakehouse/index.md) | 40h | M03, M06 |
| M12 | [Qualidade, Testes e Observabilidade de Dados](../modulos/12-qualidade-observabilidade/index.md) | 25h | M07, M09 |
| M13 | [DataOps, CI/CD e Infraestrutura como Código](../modulos/13-dataops-cicd-iac/index.md) | 25h | M10, M12 |
| M14 | [Governança, Segurança e LGPD/GDPR](../modulos/14-governanca-seguranca-lgpd/index.md) | 20h | M06 |

## Eixo 5 — Carreira e Integração (80h)

| # | Disciplina | CH | Pré-requisitos |
|---|---|---|---|
| M15 | [Carreira, Portfólio e Preparação para Entrevistas](../modulos/15-carreira-portfolio-entrevistas/index.md) | 20h | Eixos 1–4 |
| TCC | [Implementação de um Data Warehouse completo](../tcc/especificacao-dw.md) | 60h | Todos |

## Consolidado

| Eixo | Carga horária |
|---|---|
| 1 — Fundamentos | 155h |
| 2 — Data Warehousing e Modelagem | 110h |
| 3 — Pipelines e Orquestração | 95h |
| 4 — Escala, Qualidade e Governança | 110h |
| 5 — Carreira e Integração (inclui TCC) | 80h |
| **Total** | **550h** |

## Projetos integradores (portfólio)

Cada eixo (1–4) encerra com um [projeto integrador](../projetos/eixo-1-fundamentos/index.md)
publicável no GitHub; o Eixo 5 culmina no **TCC**.

---
**Revisado em:** 2026-08-20
