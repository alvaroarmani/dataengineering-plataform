# Lab 01 — dbt na bancada: seu primeiro build (walkthrough guiado)

**Onde roda:** 🐳 Bancada Docker (dbt real sobre Postgres). É um passo a passo real — confira
os **self-checks** ✅. Depois, o [Exercício 01](exercicio-01.md) pede para você completar um model.

---

## 0. Suba a bancada (uma vez)
```bash
cd ambiente && cp .env.example .env && docker compose up -d
docker compose ps        # postgres deve estar "healthy"
```
✅ *Self-check:* `postgres` aparece como `running`/`healthy`.

---

## 1. Conheça o mini-projeto
O projeto vive em `modulos/07-transformacao-dbt/exercicio-01/projeto_dbt/`:
```
projeto_dbt/
├── dbt_project.yml      # nome, profile, materialização padrão (view)
├── profiles.yml         # conexão com o Postgres da bancada (via env)
├── seeds/raw_pedidos.csv# dados crus versionados
└── models/
    ├── sources.yml      # declara a fonte 'olist.raw_pedidos'
    ├── stg_pedidos.sql  # o model de staging (você completa no Ex. 01)
    └── schema.yml       # testes: not_null, unique
```

---

## 2. Verifique a conexão (debug)
```bash
cd ambiente
docker compose --profile dbt run --rm dbt debug \
  --project-dir  modulos/07-transformacao-dbt/exercicio-01/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-01/projeto_dbt
```
✅ *Self-check:* "Connection test: OK" (o dbt fala com o Postgres).

---

## 3. Rode o build (seed → run → test)
```bash
docker compose --profile dbt run --rm dbt build \
  --project-dir  modulos/07-transformacao-dbt/exercicio-01/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-01/projeto_dbt
```
O `build` carrega o seed (`raw_pedidos`), materializa `stg_pedidos` e roda os testes.

✅ *Self-check:* linhas `PASS`/`OK` — e você vê o **DAG** rodando `seed → model → test`.
> Com o model ainda incompleto (Ex. 01), alguns testes podem falhar — é esse verde que você vai buscar.

---

## 4. Espie o resultado no Postgres
```bash
docker compose exec postgres psql -U curso -d curso -c "SELECT * FROM stg_pedidos;"
```
✅ *Self-check:* aparece a tabela `stg_pedidos` (uma **view** criada pelo dbt).

---

## O que você levou daqui
Rodou o dbt de verdade contra um Postgres real: `seed`, `run`, `test` e o **DAG** na ordem
certa. No [Exercício 01](exercicio-01.md) você completa o model de staging até o build ficar
100% verde; sem bancada, use o [Exercício 02](exercicio-02.md) (mesma lógica, no navegador).

---
**Revisado em:** 2026-08-24
