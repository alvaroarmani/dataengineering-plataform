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
1. Conceitos e arquiteturas de DW (Inmon vs Kimball).
2. Colunar, compressão, particionamento e clustering.
3. Prática no BigQuery (carga + modelagem).
4. Custos e otimização; panorama de DWs cloud.

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
