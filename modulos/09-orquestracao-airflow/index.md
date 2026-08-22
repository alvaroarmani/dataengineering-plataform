# Módulo 09 — Orquestração de Workflows com Apache Airflow

> Agendar, coordenar e monitorar pipelines de forma idempotente e observável.

## Identificação
- **Eixo:** 3 — Pipelines e Orquestração
- **Carga horária:** 40h
- **Pré-requisitos:** M03, M08
- **Onde roda:** Bancada Docker (Airflow via compose)

## Ementa
Conceitos de orquestração e DAGs. Anatomia do Airflow: scheduler, executor, workers,
metadata DB. Operators, tasks, dependências e sensors. Scheduling e backfill. Passagem de
dados (XComs) e boas práticas. Idempotência e reprocessamento seguro. Observabilidade
(logs, retries, alertas). Deploy do Airflow com Docker.

## Competências e habilidades
- C8 — orquestrar workflows com Airflow (idempotência, observabilidade).

## Objetivos de aprendizagem
1. **Escrever** uma DAG com dependências e agendamento.
2. **Garantir** idempotência e reprocessamento seguro (backfill).
3. **Configurar** retries, logs e alertas.
4. **Subir** o Airflow com Docker.

## Plano de aulas (unidades)
1. Orquestração e DAGs; arquitetura do Airflow.
2. Operators, tasks, sensors, dependências.
3. Scheduling, backfill e idempotência.
4. Observabilidade e deploy com Docker.

## Metodologia e avaliação
**Maestria:** DAG idempotente e agendada que reprocessa um dia sem duplicar, conforme rubrica.

## O que o mercado espera
Airflow é o orquestrador mais pedido; idempotência é sinal de maturidade.

## Erros comuns
- DAGs não idempotentes (reprocessar duplica dados).
- Lógica pesada dentro da DAG em vez de tasks isoladas.
- Ignorar retries e alertas.

## Recursos
A curar em `recursos.md` (docs do Airflow; Astronomer Airflow Fundamentals).

---
**Revisado em:** 2026-08-20
