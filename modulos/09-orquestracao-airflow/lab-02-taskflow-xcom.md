# Lab 02 — TaskFlow API e XCom (walkthrough guiado)

**Onde roda:** 🐳 Bancada Docker (Airflow real). Confira os **self-checks** ✅. A lógica de
XCom e sensor você fixa nos [Exercícios 03](exercicio-03.md) e [04](exercicio-04.md).

A DAG está em [`dags/dag_taskflow.py`](dags/dag_taskflow.py): `extrair → somar → reportar`,
com o valor fluindo por **XCom**.

---

## 1. Suba o Airflow (se ainda não estiver)
```bash
cd ambiente && docker compose --profile airflow up -d
```
✅ *Self-check:* na UI (http://localhost:8080) aparece a DAG **`pipeline_taskflow`**.

---

## 2. Rode e veja o XCom fluir
```bash
docker compose exec airflow airflow dags test pipeline_taskflow 2026-01-01
```
✅ *Self-check:* a saída mostra `extrair` → `somar` → `reportar`, terminando com `total = 10`
(1+2+3+4). O `reportar` recebeu o resultado de `somar` **via XCom**, sem você declarar a
dependência manualmente — a TaskFlow API infere pela passagem do valor.

---

## 3. Inspecione o XCom na UI
Na UI, abra `pipeline_taskflow` → uma execução → clique na task `somar` → aba **XCom**: veja o
valor `10` que ela "retornou" (e que `reportar` consumiu).

✅ *Self-check:* o XCom da task `somar` mostra `10`.

---

## O que você levou daqui
Escreveu/rodou uma DAG no estilo **TaskFlow** (`@task`), com dependências inferidas e **XCom
implícito** no `return`. Agora fixe a mecânica de XCom e de **sensor** nos
[Exercícios 03](exercicio-03.md) e [04](exercicio-04.md).

---
**Revisado em:** 2026-08-29
