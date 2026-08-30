# Lab 03 — Backfill idempotente (walkthrough guiado)

**Onde roda:** 🐳 Bancada Docker (Airflow real). Confira os **self-checks** ✅. A lógica de
idempotência você fixa nos [Exercícios 05](exercicio-05.md) (Postgres real) e [06](exercicio-06.md).

Usa a DAG `pipeline_exemplo` (`@daily`) do [Lab 01](lab-01-airflow-na-bancada.md).

---

## 1. Rode uma data específica (data lógica)
```bash
cd ambiente
docker compose exec airflow airflow dags test pipeline_exemplo 2026-01-10
```
✅ *Self-check:* a execução roda para **2026-01-10** (a data lógica), não para "agora".

---

## 2. Backfill de um intervalo
Reprocesse vários dias de propósito:
```bash
docker compose exec airflow airflow dags backfill \
  -s 2026-01-08 -e 2026-01-10 pipeline_exemplo
```
✅ *Self-check:* o Airflow roda 2026-01-08, 09 e 10 — cada execução dona do seu dia.

---

## 3. Idempotência: rode a MESMA data de novo
```bash
docker compose exec airflow airflow dags test pipeline_exemplo 2026-01-10
```
Numa DAG idempotente (carga por **overwrite da partição** ou **upsert**), reprocessar
2026-01-10 **substitui** os dados daquele dia — não duplica.

✅ *Self-check:* rodar 2x a mesma data leva ao **mesmo estado** (é isso que o Exercício 05
prova no Postgres, rodando a carga duas vezes).

---

## O que você levou daqui
Rodou por **data lógica**, fez **backfill** de um intervalo e viu por que a carga precisa ser
**idempotente**. Prove a idempotência no [Exercício 05](exercicio-05.md) (DELETE+INSERT do dia
no Postgres real) e no [06](exercicio-06.md) (em memória).

---
**Revisado em:** 2026-08-29
