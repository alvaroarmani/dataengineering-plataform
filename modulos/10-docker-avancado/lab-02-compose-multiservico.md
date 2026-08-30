# Lab 02 — Compose multi-serviço: redes e volumes (walkthrough guiado)

**Onde roda:** 🐳 Docker na sua máquina. Confira os **self-checks** ✅. A lógica (ordem de
subida, portas) você fixa nos [Exercícios 03](exercicio-03.md) e [04](exercicio-04.md).

Usa a bancada do curso: [`ambiente/docker-compose.yml`](../../ambiente/docker-compose.yml)
(jupyter + postgres + minio na mesma rede, com volumes).

---

## 1. Suba o stack
```bash
cd ambiente && cp .env.example .env
docker compose up -d
docker compose ps
```
✅ *Self-check:* `postgres` (healthy), `jupyter` e `minio` aparecem `running`.

---

## 2. Rede: um serviço acha o outro pelo NOME
```bash
docker compose exec postgres pg_isready -h postgres        # o host é o NOME do serviço
docker compose exec jupyter bash -lc "getent hosts postgres"
```
✅ *Self-check:* de dentro do Jupyter, o host `postgres` resolve (mesma rede). `localhost` ali
seria o próprio Jupyter — por isso a app usa `postgres:5432`, não `localhost`.

---

## 3. Volume: os dados persistem
```bash
docker compose exec postgres psql -U curso -d curso -c "CREATE TABLE t(x int); INSERT INTO t VALUES (42);"
docker compose restart postgres
docker compose exec postgres psql -U curso -d curso -c "SELECT * FROM t;"
```
✅ *Self-check:* o `42` continua lá após o restart — porque `pgdata` é um **named volume**.
```bash
docker volume ls | grep -i data      # pgdata / miniodata existem
```

---

## 4. Portas: host ↔ container
```bash
docker compose port minio 9001        # console do MinIO publicado no host
```
Abra o host mostrado (ex.: http://localhost:9001).
✅ *Self-check:* o console do MinIO abre — a porta 9001 do container está publicada no host.

---

## O que você levou daqui
Subiu um **stack multi-serviço** com Compose, viu **rede** (resolução por nome), **volume**
(persistência após restart) e **portas** (host↔container). Fixe a lógica nos
[Exercícios 03](exercicio-03.md) e [04](exercicio-04.md).

> Derrubar mantendo os dados: `docker compose down` · apagar dados: `docker compose down -v`.

---
**Revisado em:** 2026-08-29
