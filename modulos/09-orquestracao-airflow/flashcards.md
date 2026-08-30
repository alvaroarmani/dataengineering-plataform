# Flashcards — Módulo 09

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Cron vs orquestrador (Airflow)? / **R:** Cron dispara um script num horário; o orquestrador gerencia dependências, retries, backfill, paralelismo, monitoramento e agendamento do pipeline inteiro.
- **P:** O que é uma DAG e por que "acíclica"? / **R:** Directed Acyclic Graph: tasks (nós) + dependências dirigidas (arestas), sem ciclos — um ciclo faria o pipeline nunca terminar.
- **P:** Como declarar dependência entre tasks no Airflow? / **R:** Com `>>`: `a >> b` faz `b` rodar depois de `a`.
- **P:** Componentes do Airflow? / **R:** Scheduler (decide o que rodar), executor/workers (executam), metadata DB (estado), webserver/UI (visualização e disparo).
- **P:** O que fazem schedule e catchup? / **R:** schedule define a periodicidade (ex.: @daily); catchup=False evita rodar todas as execuções passadas ao ligar a DAG.
- **P:** Em que ordem o Airflow roda as tasks? / **R:** Ordem topológica (dependências primeiro), paralelizando o que é independente — algoritmo de Kahn.
- **P:** Onde NÃO colocar lógica pesada? / **R:** No topo do arquivo da DAG (é lido a cada scan do scheduler); a lógica vai dentro das tasks.

---
**Revisado em:** 2026-08-29
