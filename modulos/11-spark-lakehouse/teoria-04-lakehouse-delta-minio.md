# Data Lake, Lakehouse e formatos de tabela (Delta/Iceberg)

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Onde o Spark lê e grava esses TBs? Num **data lake** — armazenamento de objetos barato
(S3/MinIO) cheio de arquivos (Parquet, M8). Mas um data lake "cru" não tem transações,
versionamento nem garantia de consistência — vira um "pântano". A resposta moderna é o
**Lakehouse**: colocar uma **camada de tabela** (Delta/Iceberg) sobre os arquivos, trazendo
**ACID, time travel e schema** para o lake. Esta unidade fecha o M11 com essa arquitetura.

## 💡 Conceito (o porquê)

### Data Lake: barato e flexível (mas cru)
Um **data lake** guarda arquivos em **object storage** (S3, GCS, Azure Blob, **MinIO** local):
barato, escala infinita, qualquer formato. Guardamos em camadas (bronze/prata/ouro, M6) e em
**Parquet** (colunar). Problema do lake cru: sem **transações** (uma escrita que falha no meio
deixa lixo), sem **versionamento**, e leituras podem pegar dados **inconsistentes**.

### Warehouse vs Lake vs Lakehouse
- **Data Warehouse:** dados modelados, ACID, ótimo para BI — mas caro e menos flexível para dados variados.
- **Data Lake:** barato e flexível — mas sem garantias (o "pântano").
- **Lakehouse:** o meio-termo — **arquivos baratos no lake + uma camada de tabela** que adiciona
  ACID, schema e performance. "O melhor dos dois".

### Formatos de tabela: Delta e Iceberg
São **camadas de metadados** sobre os arquivos Parquet que transformam uma pasta de arquivos
numa **tabela** com garantias:
- **ACID:** escritas atômicas (ou tudo, ou nada) — sem leituras vendo dados pela metade.
- **Time travel:** consultar a tabela **como era** numa versão/hora anterior (auditoria, rollback).
- **Schema enforcement/evolution:** rejeita dados fora do schema; evolui com segurança (M8).
- **Upserts/`MERGE` e deletes:** operações que um lake cru não tem (ex.: aplicar CDC, apagar por LGPD).
- **Delta Lake** (Databricks) e **Apache Iceberg** são os principais; a ideia é a mesma.

### Como funciona (por baixo)
Além dos Parquet, há um **log de transações** (arquivos de metadados) que registra cada versão
da tabela — quais arquivos compõem cada *snapshot*. Ler a tabela = consultar o log para saber
os arquivos válidos daquela versão. É isso que dá ACID e time travel sem banco central.

## 🔎 Exemplo
No lakehouse local do curso: o Spark grava uma tabela **Delta** no **MinIO** (`s3a://.../vendas`).
Uma carga que falha no meio **não corrompe** a tabela (ACID). Amanhã, um `MERGE` aplica as
mudanças do dia (upsert idempotente, M8/M9). Se alguém subir dado errado, você faz **time
travel** para a versão anterior e corrige. Tudo sobre arquivos Parquet baratos — sem um DW caro.

:::{admonition} 📖 Da literatura
:class: seealso
Armbrust et al. descrevem o **Delta Lake**: uma camada de armazenamento de tabelas ACID sobre
object storage, usando um **log de transações** para dar atomicidade, versionamento (time
travel) e schema — resolvendo os problemas do data lake cru. — *Delta Lake: High-Performance
ACID Table Storage over Cloud Object Stores* (2020).
:::

:::{admonition} 🏭 Do mundo real
:class: important
Reis & Housley apontam o **lakehouse** como convergência dominante: a economia/flexibilidade do
lake com as garantias do warehouse, via formatos como Delta/Iceberg. MinIO oferece uma API S3
local para praticar isso sem cloud. — *Fundamentals of Data Engineering* (armazenamento).
:::

## ⚠️ Erros comuns
- Tratar um **data lake cru** como se tivesse transações — escritas parciais deixam lixo e leituras inconsistentes.
- Guardar tudo em **CSV** no lake em vez de Parquet — lento e caro (M8).
- Confundir **formato de arquivo** (Parquet) com **formato de tabela** (Delta/Iceberg) — o segundo é a camada de metadados/ACID por cima.
- Ignorar **manutenção** (compactar arquivos pequenos, `VACUUM`) — muitos arquivinhos degradam a performance.
- Achar que lakehouse dispensa modelagem — o star schema (M5) continua valendo nas camadas de consumo.

## 💼 O que o mercado espera
Explicar warehouse vs lake vs lakehouse, e o que Delta/Iceberg agregam (ACID, time travel,
MERGE) é assunto quente. Saber que o lakehouse usa object storage + camada de tabela mostra
visão de arquitetura moderna.

:::{admonition} ✨ Em resumo
:class: resumo
- **Data lake** = arquivos baratos em object storage (S3/MinIO); flexível, mas cru (sem ACID/versão).
- **Lakehouse** = lake + **camada de tabela** (Delta/Iceberg) → ACID, **time travel**, schema, `MERGE`/deletes.
- É o meio-termo entre a flexibilidade/custo do lake e as garantias do warehouse.
- Por baixo: Parquet + um **log de transações** que versiona os snapshots da tabela.
:::

## 🧠 Quiz de recall
1. O que é um data lake e qual seu problema quando "cru"?
   :::{dropdown} Resposta
   Arquivos em object storage barato (S3/MinIO), flexível e escalável; cru, não tem transações, versionamento nem garantia de consistência (vira "pântano").
   :::
2. O que é um lakehouse?
   :::{dropdown} Resposta
   Uma camada de tabela (Delta/Iceberg) sobre os arquivos do lake, adicionando ACID, schema e performance — a economia do lake com as garantias do warehouse.
   :::
3. O que Delta/Iceberg agregam sobre Parquet cru?
   :::{dropdown} Resposta
   ACID (escritas atômicas), time travel (versões anteriores), schema enforcement/evolution e operações como MERGE/upsert e delete.
   :::
4. Diferença entre formato de arquivo e formato de tabela?
   :::{dropdown} Resposta
   Parquet é formato de arquivo (colunar); Delta/Iceberg são formatos de tabela — uma camada de metadados/log de transações sobre os Parquet que dá ACID/versionamento.
   :::
5. Para que serve o time travel?
   :::{dropdown} Resposta
   Consultar a tabela como era numa versão/hora anterior — auditoria, depuração e rollback de dados errados.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Warehouse, lake ou lakehouse — quando cada um?"
  :::{dropdown} Resposta modelo
  Warehouse para BI modelado com ACID e simplicidade (custo maior). Lake para guardar tudo barato e flexível (dados variados, ML), aceitando a falta de garantias. Lakehouse quando quero as duas coisas: arquivos baratos no object storage com uma camada Delta/Iceberg dando ACID, time travel e MERGE.
  :::
- **P:** "O que o Delta Lake resolve num data lake?"
  :::{dropdown} Resposta modelo
  A falta de transações e versionamento: com um log de transações sobre os Parquet, ele dá escritas atômicas (sem lixo de escrita parcial), leituras consistentes, time travel e operações de MERGE/delete — essenciais para CDC e para apagar dados por LGPD.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Armbrust et al. — Delta Lake** (2020), o paper.
- **Reis & Housley — Fundamentals of Data Engineering** (data lake, lakehouse, object storage).
- **Apache Iceberg / Delta Lake docs** (formatos de tabela).

## 📚 Referências
- Armbrust, M. et al. *Delta Lake: ACID Table Storage over Cloud Object Stores* (2020). <!-- @armbrust2020 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — lake, lakehouse, armazenamento. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 3/10 (armazenamento, batch). <!-- @kleppmann2017 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
