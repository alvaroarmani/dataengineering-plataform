# Recursos — Módulo 06 (Data Warehousing + BigQuery)

Curadoria de fontes. Todas registradas em [`referencias.yaml`](../../referencias.yaml).

## Livros
- **Reis, J.; Housley, M. — Fundamentals of Data Engineering** (2022), cap. 8: arquiteturas de DW, Inmon vs Kimball, camadas.
- **Kleppmann, M. — Designing Data-Intensive Applications** (2017), cap. 3: data warehousing, OLTP vs OLAP, armazenamento colunar.
- **Kimball, R.; Ross, M. — The Data Warehouse Toolkit** (2013): bus architecture, dimensões conformadas.
- **Inmon, W. H. — Building the Data Warehouse** (2005): a abordagem top-down (EDW normalizado / CIF).

## Documentação oficial
- **BigQuery** — <https://cloud.google.com/bigquery/docs> (carga, particionamento, clustering, custos).

## Prática
- **BigQuery sandbox / free tier** — permite consultar sem cartão (cotas gratuitas de armazenamento e consulta).
- **Dataset Olist** — ver [`datasets/README.md`](../../datasets/README.md) para carregar no BigQuery.

> **Custo:** o BigQuery cobra por dados **varridos** na consulta. Evite `SELECT *`, use
> partição/cluster e a estimativa de bytes do editor antes de rodar.

---
**Revisado em:** 2026-08-23
