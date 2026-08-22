# Catálogo de Datasets

Usamos **dados reais** desde o início — é o que prepara você para o mercado. Arquivos
grandes **não** ficam no git (ver `.gitignore`); esta página diz como obtê-los.

## Datasets do curso

### 1. NYC Taxi Trips (fato clássico de DE)
Corridas de táxi de Nova York — grande, colunar, ótimo para agregações e particionamento.

- **Formato:** Parquet (mensal).
- **Fonte:** <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page>
- **Uso:** M03 (pandas), M06 (DW/BigQuery), M11 (Spark), TCC.

### 2. Olist — E-commerce Brasileiro
Pedidos reais de e-commerce (clientes, itens, pagamentos, reviews) — perfeito para
**modelagem dimensional** (star schema) e para o TCC.

- **Formato:** CSV (vários arquivos relacionados).
- **Fonte:** Kaggle — "Brazilian E-Commerce Public Dataset by Olist".
- **Uso:** M04 (SQL), M05 (modelagem), M07 (dbt), TCC.

### 3. APIs públicas (ingestão)
Para praticar ingestão via API (batch/incremental).

- **Exemplos:** Banco Central (câmbio/SGS), IBGE, OpenWeather.
- **Uso:** M08 (ingestão), M09 (Airflow).

## Convenções
- Baixe para `datasets/data/` (ignorado pelo git).
- Cada módulo que usa um dataset traz um script/nota de download reproduzível.
- Para exemplos pequenos versionáveis, use nomes `exemplo-*.csv` (permitidos no `.gitignore`).

---
**Revisado em:** 2026-08-20
