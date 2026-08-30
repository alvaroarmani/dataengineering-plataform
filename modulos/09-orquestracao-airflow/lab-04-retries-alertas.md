# Lab 04 — Retries e alertas (walkthrough guiado)

**Onde roda:** 🐳 Bancada Docker (Airflow real). Confira os **self-checks** ✅. A lógica de
retries e do estado do run você fixa nos [Exercícios 07](exercicio-07.md) e [08](exercicio-08.md).

---

## 1. Uma DAG com retry e alerta de falha
Crie `modulos/09-orquestracao-airflow/dags/dag_falha.py`:
```python
import datetime as dt
from airflow import DAG
from airflow.operators.bash import BashOperator

def avisar(context):
    ti = context["task_instance"]
    print(f"[ALERTA] {ti.task_id} falhou em {context['ds']}")   # aqui iria Slack/e-mail

with DAG(
    dag_id="dag_falha",
    start_date=dt.datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2, "retry_delay": dt.timedelta(seconds=5),
                  "on_failure_callback": avisar},
    tags=["curso", "m09"],
) as dag:
    quebra = BashOperator(task_id="quebra", bash_command="exit 1")   # falha de propósito
```

## 2. Rode e veja o retry + alerta
```bash
cd ambiente
docker compose exec airflow airflow dags test dag_falha 2026-01-01
```
✅ *Self-check:* a task `quebra` é tentada **3 vezes** (1 + 2 retries) e, ao esgotar, o
`on_failure_callback` imprime `[ALERTA] quebra falhou...`. Na UI, a task fica **vermelha** com os
logs das tentativas.

---

## 3. Logs: a 1ª parada do debug
Na UI (http://localhost:8080) → `dag_falha` → a execução → task `quebra` → **Logs**: veja cada
tentativa e o erro (`exit 1`).

✅ *Self-check:* os logs mostram as tentativas e a mensagem do alerta.

---

## 4. Deploy: você já está rodando um
A bancada **é** um deploy do Airflow com Docker: scheduler + webserver + workers (LocalExecutor)
+ Postgres (metadata), tudo no `docker-compose.yml` (profile `airflow`), com as DAGs versionadas
em `dags/`. Em produção, troca-se o executor (Celery/K8s) e escalam-se os workers.

✅ *Self-check:* `docker compose ps` mostra `airflow` e `postgres` de pé.

---

## O que você levou daqui
Configurou **retries** e **alerta de falha** (`on_failure_callback`), leu **logs**, e entendeu
o **deploy** (processos + Docker). Fixe a mecânica nos [Exercícios 07](exercicio-07.md) e
[08](exercicio-08.md).

> Para derrubar: `docker compose --profile airflow down`.

---
**Revisado em:** 2026-08-29
