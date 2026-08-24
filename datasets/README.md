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

## Fluxo reproduzível (scripts)

O manifesto [`manifest.yaml`](manifest.yaml) é a fonte única. Dois scripts:

```bash
# 1) baixar (URL direta quando existe; ex.: NYC Taxi)
python datasets/baixar.py            # todos    |    python datasets/baixar.py nyc_taxi

# 2) carregar no Postgres da bancada (schema raw) — precisa da bancada de pé
cd ambiente && cp .env.example .env && docker compose up -d && cd ..
pip install psycopg2-binary pyyaml
python datasets/carregar_postgres.py olist
```

### Olist (Kaggle exige login)
O Olist vem do Kaggle (autenticação). Opções:
1. Baixe o zip manualmente e extraia os CSV para `datasets/data/olist/` (nomes conforme o `manifest.yaml`).
2. Ou aponte um mirror próprio: `OLIST_URL=<url> python datasets/baixar.py olist`.

## Convenções
- Baixe para `datasets/data/` (ignorado pelo git).
- Track **browser** (fundamentos): labs usam amostras pequenas embutidas ou `exemplo-*.csv`.
- Track **real** (M06+): use os datasets completos carregados na bancada (Postgres/MinIO).
- Para exemplos pequenos versionáveis, use nomes `exemplo-*.csv` (permitidos no `.gitignore`).

---
**Revisado em:** 2026-08-24
