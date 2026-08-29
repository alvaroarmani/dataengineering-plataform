# Lab 04 — Snapshots (SCD2) e docs/lineage (walkthrough guiado)

**Onde roda:** 🐳 Bancada Docker (dbt real). Confira os **self-checks** ✅. Usa o projeto de
[`exercicio-05/projeto_dbt/`](exercicio-05/projeto_dbt/) (tem `raw_produtos`).

---

## 1. Crie um snapshot (SCD2 automático)
Crie `modulos/07-transformacao-dbt/exercicio-05/projeto_dbt/snapshots/snap_produtos.sql`:
```sql
{% snapshot snap_produtos %}
{{ config(
    target_schema='snapshots',
    unique_key='produto_id',
    strategy='check',
    check_cols=['categoria']
) }}
select * from {{ source('olist', 'raw_produtos') }}
{% endsnapshot %}
```
Rode (com a bancada de pé e o seed já carregado por um `dbt build`):
```bash
cd ambiente
docker compose --profile dbt run --rm dbt snapshot \
  --project-dir  modulos/07-transformacao-dbt/exercicio-05/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-05/projeto_dbt
```
✅ *Self-check:* cria `snapshots.snap_produtos` com `dbt_valid_from`/`dbt_valid_to`/`dbt_scd_id`.

---

## 2. Provoque uma mudança e versione
Edite `seeds/raw_produtos.csv` mudando a categoria de `p3` (`casa` → `moveis`), recarregue o
seed e rode o snapshot de novo:
```bash
docker compose --profile dbt run --rm dbt seed \
  --project-dir  modulos/07-transformacao-dbt/exercicio-05/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-05/projeto_dbt
docker compose --profile dbt run --rm dbt snapshot \
  --project-dir  modulos/07-transformacao-dbt/exercicio-05/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-05/projeto_dbt
```
```bash
docker compose exec postgres psql -U curso -d curso -c \
  "SELECT produto_id, categoria, dbt_valid_from, dbt_valid_to FROM snapshots.snap_produtos WHERE produto_id='p3' ORDER BY dbt_valid_from;"
```
✅ *Self-check:* `p3` tem **duas linhas** — a de `casa` fechada (`dbt_valid_to` preenchido) e a
de `moveis` corrente (`dbt_valid_to` nulo). Isto é SCD2 automático.

---

## 3. Docs e lineage
```bash
docker compose --profile dbt run --rm dbt docs generate \
  --project-dir  modulos/07-transformacao-dbt/exercicio-05/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-05/projeto_dbt
```
✅ *Self-check:* gera `target/catalog.json` e `target/manifest.json` (o lineage está aí). Para
ver o grafo interativo, rode `dbt docs serve` numa máquina com navegador.

---

## O que você levou daqui
Rodou um **snapshot** (SCD2 automático, com colunas de vigência) e gerou **docs/lineage**. Os
[Exercícios 07](exercicio-07.md) e [08](exercicio-08.md) fixam a lógica de snapshot e de macros
no navegador.

---
**Revisado em:** 2026-08-24
