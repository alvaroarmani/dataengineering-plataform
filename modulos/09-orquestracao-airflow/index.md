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

**Unidade 1 — Orquestração, DAGs e arquitetura do Airflow**
1. **Teoria:** [Orquestração, DAGs e arquitetura](teoria-01-orquestracao-dags-airflow.md)
2. **Lab (🐳 Airflow real):** [Airflow na bancada: sua primeira DAG](lab-01-airflow-na-bancada.md)
3. **Exercícios:** [Ordem topológica (🟢)](exercicio-01.md) · [Detectar ciclo (🟢)](exercicio-02.md)

**Unidade 2 — Operators, tasks, sensors e XComs**
1. **Teoria:** [Operators, sensors e XComs](teoria-02-operators-sensors-xcoms.md)
2. **Lab (🐳 Airflow real):** [TaskFlow API e XCom](lab-02-taskflow-xcom.md)
3. **Exercícios:** [XCom entre tasks (🟢)](exercicio-03.md) · [Sensor: poke até liberar (🟢)](exercicio-04.md)

**Unidade 3 — Scheduling, backfill e idempotência**
1. **Teoria:** [Scheduling, backfill e idempotência](teoria-03-scheduling-backfill-idempotencia.md)
2. **Lab (🐳 Airflow real):** [Backfill idempotente](lab-03-backfill-idempotente.md)
3. **Exercícios:** [Carga idempotente do dia (🐳 Postgres real)](exercicio-05.md) · [Overwrite em Python (🟢)](exercicio-06.md)

_Próxima unidade (em construção): observabilidade (logs, retries, alertas) e deploy com Docker._

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
