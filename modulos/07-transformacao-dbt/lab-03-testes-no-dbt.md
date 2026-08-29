# Lab 03 — Testes no dbt: veja um teste falhar e passar (guiado)

**Onde roda:** 🐳 Bancada Docker (dbt real). Confira os **self-checks** ✅. Depois, o
[Exercício 05](exercicio-05.md) pede para você adicionar o teste `relationships`.

Usa o projeto de [`exercicio-05/projeto_dbt/`](exercicio-05/projeto_dbt/) (`dim_produto`,
`fct_itens`).

---

## 1. Rode os testes existentes
```bash
cd ambiente && docker compose up -d
docker compose --profile dbt run --rm dbt build \
  --project-dir  modulos/07-transformacao-dbt/exercicio-05/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-05/projeto_dbt
```
✅ *Self-check:* `PASS` nos testes `not_null`/`unique` de `dim_produto` e `fct_itens`.

---

## 2. Provoque uma falha (para ver o teste funcionando)
Adicione, no `seeds/raw_itens.csv`, uma linha com um produto **inexistente** na dimensão:
```
9,p999,10.0
```
Depois de adicionar o teste `relationships` (Exercício 05) e rodar o build de novo:
```bash
docker compose --profile dbt run --rm dbt build \
  --project-dir  modulos/07-transformacao-dbt/exercicio-05/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-05/projeto_dbt
```
✅ *Self-check:* o teste `relationships` **FALHA** com "Got 1 result" — o fato órfão (`p999`)
foi pego. Remova a linha e o build volta a ficar verde.

---

## 3. Um teste singular (custom)
Crie `modulos/07-transformacao-dbt/exercicio-05/projeto_dbt/tests/receita_nao_negativa.sql`:
```sql
select * from {{ ref('fct_itens') }} where price < 0
```
Rode `dbt test`. Com dados bons, retorna 0 linhas → **PASS**.

✅ *Self-check:* o teste singular aparece na saída do `dbt test` como `PASS`.

---

## O que você levou daqui
Viu que um teste dbt é **uma query que busca violações** (0 = passa), provocou uma falha de
integridade referencial de propósito e escreveu um teste singular. No [Exercício 05](exercicio-05.md)
você declara o `relationships`; no [Exercício 06](exercicio-06.md), implementa a lógica em Python.

---
**Revisado em:** 2026-08-24
