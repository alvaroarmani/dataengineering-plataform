# Módulo 23 — APIs, Microserviços e Integração de Dados

> Como os dados **entram e saem** dos sistemas: APIs REST (consumir e servir), microserviços e
> integração orientada a eventos, e os padrões de resiliência (idempotência, retry, Saga) que
> mantêm tudo confiável. A "cola" entre o seu pipeline e o resto da empresa.

## Identificação
- **Eixo:** 3 — Pipelines e Orquestração
- **Carga horária:** 25h
- **Pré-requisitos:** M03 (Python), M08 (Ingestão), M17 (Streaming)
- **Onde roda:** 🟢 Browser (lógica de integração em Python)

## Ementa
APIs REST para dados: recursos/verbos, status codes, paginação, autenticação, rate limits e
contratos — consumir e **servir** dados. Microserviços vs monólito; comunicação **síncrona
(REST/RPC)** vs **assíncrona (eventos)**; filas de tarefas (RabbitMQ) vs log de eventos (Kafka);
produtor/consumidor. Resiliência na integração: **idempotência** (Idempotency-Key), **retry com
backoff**, circuit breaker, e o padrão **Saga** (compensações) para transações entre serviços.

## Competências e habilidades
- C21 — integrar dados via APIs e eventos com padrões de resiliência.

## Objetivos de aprendizagem
1. **Consumir** APIs (paginação, status, auth) e **servir** dados com contrato.
2. **Distinguir** síncrono × assíncrono e escolher fila × log de eventos.
3. **Aplicar** idempotência e retry com backoff.
4. **Explicar** o padrão Saga para transações entre serviços.

## Plano de aulas (unidades)

**Unidade 1 — APIs REST para dados**
1. **Teoria:** [APIs REST: consumir e servir](teoria-01-apis-rest-dados.md)
2. **Exercícios:** [API de pedidos: status e precedência (🟢)](exercicio-01.md) · [Paginação: offset x cursor (🟢)](exercicio-02.md) · [Evolução de contrato e versionamento (🟢)](exercicio-06.md)

**Unidade 2 — Microserviços e event-driven**
1. **Teoria:** [Microserviços e integração orientada a eventos](teoria-02-microservicos-event-driven.md)
2. **Exercícios:** [Idempotency-Key do lado do servidor (🟢)](exercicio-03.md)

**Unidade 3 — Resiliência na integração**
1. **Teoria:** [Idempotência, retry e Saga](teoria-03-resiliencia-integracao.md)
2. **Exercícios:** [Política de retry com backoff e Retry-After (🟢)](exercicio-04.md) · [Saga orquestrada com ponto sem volta (🟢)](exercicio-05.md)

> **Módulo completo.** Liga o pipeline ao resto do sistema — a integração que falta entre os dados e as aplicações.

## Metodologia e avaliação
**Maestria:** consumir uma API paginada tratando status, explicar síncrono×assíncrono e o broker
certo, e aplicar idempotência/retry/Saga — conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Integração via API/eventos com resiliência é pão-com-manteiga de vagas de dados; idempotência,
retry e Saga aparecem em system design de integração.

## Erros comuns
- Não paginar / ignorar status codes ao consumir API.
- Fazer tudo síncrono (acoplamento e efeito dominó).
- Retry sem idempotência (duplica) ou retry no 4xx.
- "Transação atômica" entre serviços em vez de Saga.

## Recursos
Ver [`recursos.md`](recursos.md) (Kleppmann cap. 4/9/11; docs RabbitMQ/Kafka; Saga; Idempotency-Key).

---
**Revisado em:** 2026-09-09
