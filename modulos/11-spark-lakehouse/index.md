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
1. Processamento distribuído; arquitetura do Spark.
2. PySpark: DataFrames, transformações e ações.
3. Partições, shuffle e otimização.
4. Data Lake/Lakehouse; Delta/Iceberg; MinIO.

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
