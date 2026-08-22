# Módulo 05 — Modelagem de Dados e Dimensional Modeling (Kimball)

> O coração do Data Warehouse: modelar fatos e dimensões para análise.

## Identificação
- **Eixo:** 2 — Data Warehousing e Modelagem
- **Carga horária:** 40h
- **Pré-requisitos:** M04
- **Onde roda:** Bancada Docker (Postgres)

## Ementa
Normalização (1FN–3FN) e por que desnormalizamos para análise. Modelagem dimensional
segundo Kimball: tabelas fato e dimensão, grão, star schema vs snowflake. Chaves substitutas
(surrogate keys). Slowly Changing Dimensions (SCD tipos 1, 2 e 3). Modelagem a partir de
processos de negócio.

## Competências e habilidades
- C4 — modelar dados dimensionalmente (Kimball).

## Objetivos de aprendizagem
1. **Definir** o grão de uma tabela fato e suas dimensões.
2. **Projetar** um star schema a partir de um processo de negócio.
3. **Implementar** surrogate keys e uma dimensão **SCD Tipo 2**.
4. **Justificar** escolhas de modelagem (star vs snowflake).

## Plano de aulas (unidades)
1. Normalização e o porquê da desnormalização analítica.
2. Fatos, dimensões e grão.
3. Star schema vs snowflake; surrogate keys.
4. SCDs (1, 2, 3) na prática.

## Metodologia e avaliação
**Maestria:** projetar e implementar um star schema (Olist) com uma SCD2, conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Saber modelar e **explicar** o porquê (grão, SCD) diferencia muito candidatos Jr.

## Erros comuns
- Não definir o **grão** antes de modelar.
- Usar chaves naturais onde surrogate keys seriam melhores.
- Ignorar mudanças históricas (SCD) nas dimensões.

## Recursos
A curar em `recursos.md` (Kimball & Ross *The Data Warehouse Toolkit*).

---
**Revisado em:** 2026-08-20
