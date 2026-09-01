# Projeto Integrador — Eixo 4 (Escala, Qualidade e Governança)

> **Processamento em escala + qualidade + CI.** Processa um dataset de corridas (estilo NYC Taxi),
> grava em **Parquet**, com **testes automáticos** e um olhar de **governança** — primeiro em
> pandas (auto-corrigível), depois em **PySpark → MinIO** (a trilha real). Fecha o Eixo 4.

## 🎯 Objetivo
Construir um processamento **confiável e escalável**:
1. **Transformar** corridas (derivar duração/data, **remover inválidas**);
2. **Agregar** por dia (corridas, receita, duração média) — pensando em **partição**;
3. **Gravar** em **Parquet** (colunar);
4. **Testes de qualidade** rodando em **CI** (portão automático) + nota de **governança/LGPD**.

## 📦 Dataset
Uma amostra estilo **NYC Taxi** (`starter/data/amostra_corridas.csv`), com corridas inválidas de
propósito. Depois, escale para **1 mês real** do NYC Taxi (ver [datasets](../../datasets/README.md))
na trilha PySpark.

## 🧭 Etapas e requisitos

**Trilha A — núcleo auto-corrigível (pandas/pyarrow).** Em `starter/processamento.py`, implemente:
- `transformar(df)` → `[data, passageiros, valor, duracao_min]`, sem corridas inválidas (`duracao_min<=0` ou `passageiros<=0`).
- `agregar_por_dia(df)` → `corridas`, `receita`, `duracao_media` por data.
- `escrever_parquet(df, caminho)` → grava colunar (Parquet).

Faça `pytest -q` passar (3 testes) e mantenha o **CI** (`.github/workflows/ci.yml`) verde.

**Trilha B — em PySpark, no MinIO (bancada Docker) 🐳.** Reescreva a transformação/agregação em
**PySpark** (`starter/spark/job_spark.py`) e grave **particionado por data** em Parquet no **MinIO**,
como no [M11](../../modulos/11-spark-lakehouse/index.md).

## ✅ Entregáveis
- Repositório **no GitHub** com a **trilha A verde**, **CI ativo** e, idealmente, o **job PySpark** (trilha B).
- **README** com **diagrama**, como rodar, achados e a **nota de governança/LGPD** (quais campos seriam pessoais e como tratá-los — M14).
- Parágrafo **Situação → Ação → Resultado** para o currículo (M15).

## 📊 Rubrica (0–100)
| Critério | Peso |
|---|---|
| Transformação correta (deriva + remove inválidas) | 25 |
| Agregação por dia (partição) + escrita Parquet | 20 |
| Testes de qualidade + **CI** verde | 25 |
| Trilha real em PySpark → MinIO | 15 |
| Documentação + nota de governança/LGPD | 15 |

Conceito mínimo para "concluído": **60**, sem nenhum critério zerado.

## 💡 Dicas (hint ladder)
:::{dropdown} Dica 1 — duração e filtro
`pd.to_datetime` nas duas colunas; `duracao_min = (dropoff - pickup).dt.total_seconds() / 60`; filtre `duracao_min > 0` e `passageiros > 0`.
:::
:::{dropdown} Dica 2 — agregação nomeada
`df.groupby("data").agg(corridas=("valor","size"), receita=("valor","sum"), duracao_media=("duracao_min","mean"))`.
:::
:::{dropdown} Dica 3 — Parquet e partição
`df.to_parquet(caminho, index=False)`; no Spark, `write.partitionBy("data").parquet(...)` para particionar (economia de custo, M21).
:::

---
**Revisado em:** 2026-08-31
