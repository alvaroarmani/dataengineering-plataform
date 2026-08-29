# Lab 03 — BigQuery na prática (walkthrough guiado)

**Onde roda:** ☁️ **BigQuery sandbox (free-tier, sem cartão)**. É um passo a passo real na
nuvem — sem correção automática; confira os **self-checks** ✅ ao final de cada etapa.
Quem ainda não quer criar conta: faça o [Exercício 03](exercicio-03.md) (mesmo raciocínio,
auto-corrigido no Postgres da bancada).

---

## 0. Criar o sandbox (uma vez, ~3 min)
1. Acesse <https://console.cloud.google.com/bigquery> e faça login com uma conta Google.
2. Aceite entrar no **BigQuery sandbox** (aparece um aviso "Sandbox" — **não** pede cartão).
3. Crie/《selecione》 um projeto (ex.: `curso-de`). No painel esquerdo você vê o **Explorer**.

✅ *Self-check:* você consegue rodar `SELECT 1 AS ok;` no editor e ver o resultado.

---

## 1. Criar um dataset
No editor de SQL, rode:
```sql
CREATE SCHEMA IF NOT EXISTS olist
OPTIONS(location = 'US');
```
✅ *Self-check:* o dataset `olist` aparece sob o seu projeto no Explorer.

---

## 2. Carregar dados
**Opção A (rápida, sem download):** crie uma tabela de amostra por SQL:
```sql
CREATE OR REPLACE TABLE olist.itens AS
SELECT * FROM UNNEST([
  STRUCT(DATE '2025-01-05' AS data_pedido, 'eletronicos' AS categoria, 'SP' AS estado, 1200.0 AS price),
  STRUCT(DATE '2025-01-20', 'livros', 'RJ', 30.0),
  STRUCT(DATE '2025-02-10', 'eletronicos', 'SP', 800.0),
  STRUCT(DATE '2024-12-15', 'livros', 'MG', 45.0)
]);
```
**Opção B (dataset real):** baixe os CSVs do Olist (ver `datasets/README.md`) e use
**Explorer → seu dataset → Create table → Upload** (ou `bq load`), formato CSV, *autodetect schema*.

✅ *Self-check:* `SELECT COUNT(*) FROM olist.itens;` retorna o número de linhas.

---

## 3. Tabela particionada + clusterizada (de verdade)
```sql
CREATE OR REPLACE TABLE olist.fato_item_pedido
PARTITION BY DATE_TRUNC(data_pedido, MONTH)
CLUSTER BY categoria, estado
AS SELECT data_pedido, categoria, estado, price FROM olist.itens;
```
✅ *Self-check:* em **Details** da tabela, aparece "Partitioned by: data_pedido (MONTH)" e
"Clustered by: categoria, estado".

---

## 4. Custo: estime antes de rodar (dry run)
No editor, cole a query abaixo e **olhe o canto superior direito**: "This query will process X".
```sql
-- barata: filtra pela coluna de partição e lê poucas colunas
SELECT categoria, SUM(price) AS receita
FROM olist.fato_item_pedido
WHERE data_pedido >= '2025-01-01' AND data_pedido < '2025-02-01'
GROUP BY categoria;
```
Agora compare com o custo estimado de:
```sql
SELECT * FROM olist.fato_item_pedido;   -- lê TODAS as colunas/partições (mais bytes)
```
✅ *Self-check:* a primeira query estima **menos bytes** que o `SELECT *`. No CLI seria
`bq query --dry_run --use_legacy_sql=false '...'`.

---

## 5. Limpeza
O sandbox expira tabelas em 60 dias, mas você pode remover agora:
```sql
DROP SCHEMA olist CASCADE;
```

---

## O que você levou daqui
Criou um DW cloud real, carregou dados, fez **partição + cluster de verdade** e usou o **dry
run** para raciocinar sobre **custo por bytes varridos** — a mentalidade que o mercado espera.
No [Exercício 03](exercicio-03.md) você fixa o raciocínio de partição/pruning com correção
automática no **Postgres real** da bancada.

---
**Revisado em:** 2026-08-24
