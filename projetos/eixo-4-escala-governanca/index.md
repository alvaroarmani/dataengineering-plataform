# Projeto Integrador — Eixo 4 (Escala, Qualidade e Governança)

> **Processamento em escala (Spark) + qualidade + CI**, com um olhar de governança.

## Objetivo
Processar um dataset grande (NYC Taxi) com **PySpark**, gravar em formato de **Lakehouse**
(Parquet/Delta em MinIO), aplicar **testes de qualidade** e automatizar com **CI**.

## Requisitos
1. Job **PySpark** que lê, transforma e agrega o dataset (particionado).
2. Escrita em **MinIO** (S3 local) em Parquet/Delta.
3. **Testes de qualidade de dados** (ex.: Great Expectations ou testes próprios).
4. **CI (GitHub Actions)** que roda os testes a cada push.
5. Nota de **governança/LGPD**: identifique dados sensíveis e como você os trataria.

## Entregáveis
- Repositório GitHub com o job, testes, workflow de CI e README.

## Rubrica
Ver [rubrica genérica](../../ppc/metodologia-e-avaliacao.md), com peso extra em **testes/qualidade**.

---
**Revisado em:** 2026-08-20
