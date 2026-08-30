# Lab 01 — PySpark na bancada (walkthrough guiado)

**Onde roda:** 🐳 Bancada Docker (Spark real, profile `spark`). Confira os **self-checks** ✅.
A lógica (lazy/ação, shuffle, agregação) você fixa nos exercícios da unidade.

Exemplo pronto em [`exemplo/job_spark.py`](exemplo/job_spark.py).

---

## 1. Suba o Spark
```bash
cd ambiente && cp .env.example .env
docker compose --profile spark up -d
docker compose ps        # spark deve aparecer running
```
✅ *Self-check:* o serviço `spark` está de pé (UI do master em http://localhost:8081).

---

## 2. Rode um job PySpark (spark-submit)
```bash
docker compose --profile spark run --rm spark \
  spark-submit /work/modulos/11-spark-lakehouse/exemplo/job_spark.py
```
✅ *Self-check:* a saída mostra a receita por categoria, com **A no topo** (10*2 + 3*4 = 32),
depois C (20) e B (5). Repare que só o `.show()` (ação) disparou todo o plano (lazy).

---

## 3. Explore o plano (lazy + Catalyst)
Edite o job adicionando um `.explain()` antes do `.show()` e rode de novo:
```python
   .orderBy(F.col("total").desc()).explain()
```
✅ *Self-check:* o plano físico aparece; procure o `HashAggregate`/`Exchange` — o **Exchange** é
o **shuffle** do `groupBy` (transformação wide).

---

## 4. (Opcional) Lakehouse: gravar no MinIO
Com o profile `minio` de pé, um job pode gravar Parquet/Delta em `s3a://...` (object storage
local). É a base do lakehouse (U4) — ACID/time travel viriam com Delta/Iceberg.

---

## O que você levou daqui
Rodou **PySpark de verdade** (spark-submit), viu a **lazy evaluation** (só a ação executa) e o
**shuffle** no plano (`Exchange`). Fixe os conceitos nos exercícios da unidade.

> Derrubar: `docker compose --profile spark down`.

---
**Revisado em:** 2026-08-29
