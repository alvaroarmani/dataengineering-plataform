# Lab 01 — Airflow na bancada: sua primeira DAG (walkthrough guiado)

**Onde roda:** 🐳 Bancada Docker (Airflow real, profile `airflow`). Confira os **self-checks** ✅.
A lógica de DAG (ordem, ciclo) você fixa nos [Exercícios 01](exercicio-01.md) e [02](exercicio-02.md).

A DAG de exemplo já está em
[`dags/dag_exemplo.py`](dags/dag_exemplo.py) (montada em `/opt/airflow/dags`).

---

## 1. Suba o Airflow
```bash
cd ambiente && cp .env.example .env
docker compose --profile airflow up -d
docker compose ps           # postgres + airflow devem aparecer
```
Abra a UI em **http://localhost:8080** (usuário/senha `admin`/`admin` do `.env`).

✅ *Self-check:* a UI carrega e você vê a DAG **`pipeline_exemplo`** na lista.

---

## 2. Veja a estrutura da DAG (sem rodar)
```bash
docker compose exec airflow airflow dags show pipeline_exemplo
docker compose exec airflow airflow tasks list pipeline_exemplo
```
✅ *Self-check:* as tasks `extrair → carregar → transformar → validar` aparecem, nessa ordem de dependência.

---

## 3. Rode uma execução de teste (sem scheduler)
`airflow dags test` executa a DAG para uma data, na hora, sem depender do agendamento:
```bash
docker compose exec airflow airflow dags test pipeline_exemplo 2026-01-01
```
✅ *Self-check:* a saída mostra cada task rodando **em ordem** e terminando em `success`.

---

## 4. Explore na UI
Na UI (http://localhost:8080), abra `pipeline_exemplo` → **Graph**: veja o grafo; clique numa
task → **Logs** para ver a saída. Dispare manualmente com o botão **Trigger DAG**.

✅ *Self-check:* o grafo mostra as 4 tasks encadeadas; os logs de cada uma trazem o `echo`.

---

## O que você levou daqui
Subiu o **Airflow real**, viu uma DAG (tasks + dependências), rodou um teste e explorou a UI
(grafo, logs). Agora fixe a **ordem topológica** e a **detecção de ciclo** (o "A" de DAG) nos
[Exercícios 01](exercicio-01.md) e [02](exercicio-02.md).

> Para derrubar: `docker compose --profile airflow down`.

---
**Revisado em:** 2026-08-29
