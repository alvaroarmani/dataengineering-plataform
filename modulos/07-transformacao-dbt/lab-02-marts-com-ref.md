# Lab 02 — Marts com ref(): montando o star (walkthrough guiado)

**Onde roda:** 🐳 Bancada Docker (dbt real). Confira os **self-checks** ✅. Depois, o
[Exercício 03](exercicio-03.md) pede para você completar o mart.

O projeto de [`exercicio-03/projeto_dbt/`](exercicio-03/projeto_dbt/) tem os staging models
prontos (`stg_itens`, `stg_produtos`) e o mart `fct_receita_categoria` a completar.

---

## 1. Veja o DAG antes de rodar
```bash
cd ambiente
docker compose --profile dbt run --rm dbt ls --resource-type model \
  --project-dir  modulos/07-transformacao-dbt/exercicio-03/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-03/projeto_dbt
```
✅ *Self-check:* aparecem `stg_itens`, `stg_produtos`, `fct_receita_categoria`.

---

## 2. Build (seed → staging → mart → testes)
```bash
docker compose --profile dbt run --rm dbt build \
  --project-dir  modulos/07-transformacao-dbt/exercicio-03/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-03/projeto_dbt
```
✅ *Self-check:* o dbt roda os **staging antes** do fato (porque o `ref()` disse a ordem) e
materializa `fct_receita_categoria` como **table**.

---

## 3. Confirme o encadeamento (lineage) e o resultado
```bash
docker compose exec postgres psql -U curso -d curso -c "SELECT * FROM fct_receita_categoria ORDER BY receita DESC;"
```
✅ *Self-check:* a tabela existe e traz a receita por categoria (livros no topo).
> `fct_receita_categoria` depende de `stg_itens` e `stg_produtos` via `ref()` — esse é o DAG
> que o dbt executa e desenha como lineage.

---

## O que você levou daqui
Viu o **DAG** (staging → mart), rodou o build na ordem certa e materializou um mart como
`table`. No [Exercício 03](exercicio-03.md) você completa o mart até o verde; sem bancada,
use o [Exercício 04](exercicio-04.md) (mesma consulta, no navegador).

---
**Revisado em:** 2026-08-24
