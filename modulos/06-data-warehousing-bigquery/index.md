# Módulo 06 — Data Warehousing: Teoria e Prática + BigQuery

> Construir um Data Warehouse na nuvem, entendendo colunar, particionamento e custos.

## Identificação
- **Eixo:** 2 — Data Warehousing e Modelagem
- **Carga horária:** 40h
- **Pré-requisitos:** M05
- **Onde roda:** BigQuery (free tier) + Bancada Docker

## Ementa
Conceitos de Data Warehouse: Inmon vs Kimball, arquitetura em camadas. Armazenamento
colunar e compressão. Particionamento e clustering. Carga e modelagem no BigQuery. Modelo
de custos (armazenamento vs consulta) e boas práticas para reduzir gastos. Comparação com
outros DWs cloud (Snowflake, Redshift) — conceitual.

## Competências e habilidades
- C5 — projetar e construir um Data Warehouse (BigQuery).

## Objetivos de aprendizagem
1. **Explicar** por que o colunar acelera análise.
2. **Carregar** e **modelar** dados no BigQuery.
3. **Aplicar** particionamento/clustering e **controlar custos**.
4. **Comparar** BigQuery com outros DWs cloud.

## Plano de aulas (unidades)

**Unidade 1 — Conceitos e arquiteturas de DW (Inmon vs Kimball)**
1. **Teoria:** [Conceitos e arquiteturas de DW](teoria-01-conceitos-arquiteturas-dw.md)
2. **Lab:** [Arquitetura em camadas (raw → core → mart)](lab-01-camadas-dw.ipynb)
3. **Exercício:** [Camadas de um DW: do raw ao mart](exercicio-01.md)

**Unidade 2 — Colunar, compressão, particionamento e clustering**
1. **Teoria:** [Por que o DW é rápido](teoria-02-colunar-particionamento.md)
2. **Lab:** [Colunar e particionamento na prática](lab-02-colunar-particionamento.ipynb)
3. **Exercício:** [Colunar e particionamento](exercicio-02.md)

**Unidade 3 — BigQuery na prática (ferramenta real, dual-track)**
1. **Teoria:** [BigQuery: serverless, carga, partição/cluster e custo](teoria-03-pratica-bigquery.md)
2. **Lab (☁️ cloud):** [BigQuery na prática — walkthrough guiado](lab-03-bigquery-na-pratica.md)
3. **Exercício (🐳 Postgres real):** [Particionamento no Postgres](exercicio-03.md)

_Próxima unidade (em construção): custos e otimização; panorama de DWs cloud._

## Metodologia e avaliação
**Maestria:** carregar o star schema no BigQuery com particionamento + consultas otimizadas, conforme rubrica.

## O que o mercado espera
Experiência com um DW cloud real e **consciência de custo** — muito valorizada.

## Erros comuns
- `SELECT *` em tabelas enormes (custo!).
- Ignorar particionamento/clustering.
- Confundir armazenamento com custo de consulta.

## Recursos
A curar em `recursos.md` (docs do BigQuery; Reis & Housley cap. armazenamento/serving).

---
**Revisado em:** 2026-08-20
