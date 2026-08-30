# Módulo 11 — Processamento em Larga Escala (Spark) + Lakehouse

> Processar dados que não cabem em uma máquina e entender a arquitetura Lakehouse.

## Identificação
- **Eixo:** 4 — Escala, Qualidade e Governança
- **Carga horária:** 40h
- **Pré-requisitos:** M03, M06
- **Onde roda:** Bancada Docker (Spark) + MinIO

## Ementa
Fundamentos de processamento distribuído (MapReduce e evolução). Apache Spark: arquitetura
(driver/executors), RDD vs DataFrame, transformações e ações, *lazy evaluation*, partições e
*shuffle*. PySpark na prática. Data Lake e Lakehouse: object storage (MinIO/S3), formatos de
tabela **Delta/Iceberg** (ACID, time travel). Noções de otimização e custo.

## Competências e habilidades
- C9 — processar dados em larga escala com Spark; entender Lakehouse.

## Objetivos de aprendizagem
1. **Explicar** o modelo de execução do Spark (lazy, partições, shuffle).
2. **Escrever** transformações e agregações com PySpark.
3. **Gravar/ler** tabelas em formato Lakehouse (Delta) sobre object storage.
4. **Discutir** trade-offs de particionamento e custo.

## Plano de aulas (unidades)

**Unidade 1 — Processamento distribuído e arquitetura do Spark**
1. **Teoria:** [Distribuído e arquitetura do Spark](teoria-01-distribuido-arquitetura-spark.md)
2. **Exercícios:** [Transformação vs ação (🟢)](exercicio-01.md) · [Quando executa — lazy (🟢)](exercicio-02.md)

**Unidade 2 — PySpark: DataFrames, transformações e ações**
1. **Teoria:** [PySpark: DataFrames](teoria-02-pyspark-dataframes.md)
2. **Lab (🐳 Spark real):** [PySpark na bancada](lab-01-pyspark-na-bancada.md)
3. **Exercícios:** [Agregação por categoria (🟢)](exercicio-03.md) · [withColumn imutável (🟢)](exercicio-04.md)

**Unidade 3 — Partições, shuffle e otimização**
1. **Teoria:** [Partições, shuffle e otimização](teoria-03-particoes-shuffle-otimizacao.md)
2. **Exercícios:** [Causa shuffle? (🟢)](exercicio-05.md) · [Contar shuffles (🟢)](exercicio-06.md)

**Unidade 4 — Data Lake, Lakehouse e Delta/Iceberg**
1. **Teoria:** [Lakehouse, Delta/Iceberg e MinIO](teoria-04-lakehouse-delta-minio.md)
2. **Exercícios:** [Time travel: versão (🟢)](exercicio-07.md) · [Schema enforcement (🟢)](exercicio-08.md)

> **Módulo completo.** Processamento em escala + lakehouse — base para o TCC com dados grandes.

## Metodologia e avaliação
**Maestria:** job PySpark que agrega um dataset grande e grava em Delta/MinIO, conforme rubrica.

## O que o mercado espera
Spark é diferencial forte para Pleno; Lakehouse é a arquitetura em ascensão.

## Erros comuns
- Fazer `collect()` de dados enormes ao driver.
- Ignorar particionamento e provocar *shuffles* caros.
- Confundir transformação (lazy) com ação.

## Recursos
A curar em `recursos.md` (docs do Spark; Delta Lake; paper MapReduce).

---
**Revisado em:** 2026-08-20
