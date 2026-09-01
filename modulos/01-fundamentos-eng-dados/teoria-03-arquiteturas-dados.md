# Arquiteturas de dados: DW, Data Lake, Lakehouse e além

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você vai ouvir uma sopa de siglas: "data warehouse", "data lake", "lakehouse", "modern data stack",
"Lambda", "Kappa", "data mesh". Cada fornecedor jura que a sua é o futuro. Para o engenheiro de dados
iniciante, isso parece um labirinto — mas por baixo há **poucas ideias** que resolvem **problemas
específicos**, e saber qual arquitetura serve a qual problema é o que se espera numa entrevista ("quando
usar data lake vs data warehouse?"). Esta unidade organiza o mapa: o que cada arquitetura é, por que
surgiu, e quando escolher cada uma — sem hype.

## 💡 Conceito (o porquê)

### Data Warehouse (DW): o analítico estruturado
O **data warehouse** é o mais antigo: um banco **analítico** (OLAP, colunar, M02-teoria) que guarda
dados **estruturados, limpos e modelados** (star schema, M05) para responder perguntas de negócio.
Força qualidade e consistência (**schema-on-write**), mas é rígido: dados não-estruturados (logs,
imagens, JSON variado) não cabem bem, e ele pode ficar caro. Ex.: BigQuery, Snowflake, Redshift.

### Data Lake: guardar tudo, barato
O **data lake** nasceu para o que o DW não abraça: um repositório de **object storage barato** (S3/GCS,
o MinIO da bancada) que guarda **qualquer coisa** no formato bruto — CSV, JSON, Parquet, imagens —
sem esquema prévio (**schema-on-read**, M18). Barato e flexível, mas sem governança vira um **"data
swamp"** (pântano): dados que ninguém acha, sem qualidade nem confiança.

### Lakehouse: o melhor dos dois
O **lakehouse** é a convergência (2020+): a **flexibilidade e o custo do lake** (object storage,
formatos abertos) **com** a **estrutura e garantias do warehouse** (tabelas, transações ACID, schema,
performance). Formatos como **Delta Lake, Iceberg e Hudi** trazem transações e versionamento sobre os
arquivos do lake. É a arquitetura dominante hoje: uma camada só, dados abertos, do bruto ao analítico.

### ETL vs ELT: a virada que a nuvem trouxe
- **ETL (Extract–Transform–Load):** transforma os dados **antes** de carregar no destino. Era a norma
  quando processar era caro e o DW, limitado.
- **ELT (Extract–Load–Transform):** carrega o dado **bruto** primeiro (no lake/warehouse barato e
  escalável) e transforma **depois, lá dentro** (com dbt, M07). A nuvem tornou o ELT o padrão: guarda
  tudo barato, transforma sob demanda, com o histórico bruto sempre disponível para reprocessar.

### Batch vs streaming e os padrões Lambda/Kappa
Já vimos batch × streaming (teoria-01, e M17). Duas arquiteturas históricas os combinam:
- **Lambda:** duas trilhas — uma **batch** (precisa, lenta) e uma **streaming** (rápida, aproximada) —
  cujos resultados se unem. Poderosa, mas complexa (dois códigos para manter).
- **Kappa:** **tudo como stream**; o batch é só um caso de reprocessar o mesmo stream. Mais simples de
  manter quando o streaming dá conta.

### Modern Data Stack e Data Mesh
- **Modern Data Stack:** não é uma arquitetura única, e sim um **conjunto de ferramentas gerenciadas**
  que se encaixam (ingestão gerenciada + warehouse na nuvem + dbt + BI), a montagem "plug-and-play" que
  o mercado usa hoje.
- **Data Mesh:** menos sobre tecnologia e mais sobre **organização** — dados como **produto**, com
  ownership por domínio (M14/M21). Uma resposta ao gargalo do time central de dados em empresas grandes.

## 🔎 Exemplo
Uma empresa moderna guarda **tudo bruto** num **data lake** (object storage barato): eventos, CSVs,
JSON de APIs. Sobre ele, uma camada **lakehouse** (Delta/Iceberg) dá tabelas com transações e schema.
O padrão é **ELT**: os dados entram brutos e são transformados **dentro** com **dbt** em camadas
staging→marts (o "warehouse" agora vive no lakehouse). Para o painel ao vivo, uma trilha **streaming**
(Kafka, M17) complementa o batch. Ferramentas gerenciadas (a **modern data stack**) costuram tudo. Uma
arquitetura, dados abertos, do bruto ao analítico — as siglas, no fim, encaixam.

:::{admonition} 📖 Da literatura
:class: seealso
Armbrust et al. formalizam o **Lakehouse** como a unificação de data lake e warehouse sobre object
storage aberto com transações. Reis & Housley mapeiam as arquiteturas (DW, lake, lakehouse, Lambda/
Kappa) e a virada ETL→ELT; Dehghani propõe o **Data Mesh** como resposta organizacional. — *Lakehouse:
A New Generation of Open Platforms*; *Fundamentals of Data Engineering*; *Data Mesh Principles*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A tendência prática é clara: **ELT sobre um lakehouse** com formatos abertos (Delta/Iceberg) virou o
padrão, porque guarda tudo barato, mantém o bruto para reprocessar e transforma sob demanda com dbt. As
siglas antigas (DW puro, lake puro) não desapareceram, mas convergem. Escolher a arquitetura é escolher
o trade-off — não seguir o hype. — Armbrust et al.; Reis & Housley.
:::

## ⚠️ Erros comuns
- **Data lake sem governança** — vira "data swamp", dados que ninguém acha nem confia.
- **DW para tudo** — tentar enfiar dados não-estruturados/variados num warehouse rígido.
- **ETL por hábito** quando ELT (carregar bruto, transformar depois) seria mais simples e barato.
- **Lambda sem necessidade** — dois códigos para manter onde Kappa (só stream) bastaria.
- **Perseguir siglas/hype** em vez de escolher pela necessidade e pelo trade-off.

## 💼 O que o mercado espera
Explicar DW × data lake × lakehouse (e quando cada um), a diferença ETL × ELT e por que a nuvem
favoreceu ELT, e ter noção de Lambda/Kappa, modern data stack e data mesh. "Quando usar data lake vs
data warehouse?" e "ETL ou ELT?" são perguntas recorrentes.

:::{admonition} ✨ Em resumo
:class: resumo
- **DW**: analítico estruturado (schema-on-write, rígido); **Data Lake**: guarda tudo bruto e barato (schema-on-read, risco de "swamp").
- **Lakehouse**: une o custo/flexibilidade do lake com a estrutura/ACID do warehouse (Delta/Iceberg) — o padrão atual.
- **ELT** (carregar bruto, transformar depois com dbt) suplantou o **ETL** na nuvem.
- **Lambda** (batch+stream) vs **Kappa** (só stream); **Modern Data Stack** = ferramentas gerenciadas; **Data Mesh** = organização (dados como produto).
:::

## 🧠 Quiz de recall
1. Qual a diferença entre data warehouse e data lake?
   :::{dropdown} Resposta
   DW guarda dados estruturados, limpos e modelados (schema-on-write, analítico rígido); data lake guarda qualquer dado bruto em object storage barato (schema-on-read, flexível, mas com risco de virar "swamp").
   :::
2. O que é um lakehouse e por que surgiu?
   :::{dropdown} Resposta
   A convergência de lake e warehouse: o custo/flexibilidade do lake com a estrutura/ACID do warehouse (via Delta/Iceberg/Hudi). Surgiu para não escolher entre barato-flexível e estruturado-confiável.
   :::
3. Qual a diferença entre ETL e ELT, e por que a nuvem favoreceu ELT?
   :::{dropdown} Resposta
   ETL transforma antes de carregar; ELT carrega o bruto primeiro e transforma depois, dentro do destino. A nuvem (armazenamento/processamento baratos e escaláveis) tornou viável guardar tudo bruto e transformar sob demanda com dbt.
   :::
4. Lambda vs Kappa?
   :::{dropdown} Resposta
   Lambda tem duas trilhas (batch precisa + streaming rápida) que se unem — poderosa mas complexa. Kappa trata tudo como stream (batch = reprocessar o stream) — mais simples quando o streaming dá conta.
   :::
5. O que é Data Mesh e como difere das demais?
   :::{dropdown} Resposta
   É uma abordagem organizacional (não uma tecnologia): dados como produto, com ownership por domínio e governança federada — resposta ao gargalo do time central de dados em grandes empresas.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Quando você usaria um data lake em vez de um data warehouse?"
  :::{dropdown} Resposta modelo
  Quando preciso guardar dados variados e brutos (logs, JSON, imagens) de forma barata e flexível, sem esquema prévio — coisas que não cabem bem num warehouse rígido. O DW brilha para o analítico estruturado e modelado. Na prática hoje uso um lakehouse: guardo tudo bruto no lake e ponho uma camada com tabelas/ACID (Delta/Iceberg) por cima, tendo os dois benefícios. E aplico governança para o lake não virar "swamp".
  :::
- **P:** "ETL ou ELT?"
  :::{dropdown} Resposta modelo
  Hoje, ELT por padrão na nuvem: carrego o dado bruto primeiro num lake/warehouse escalável e transformo depois, dentro, com dbt. Isso mantém o histórico bruto para reprocessar, é mais barato e desacopla ingestão de transformação. ETL ainda faz sentido quando preciso transformar/filtrar antes por custo, compliance (não guardar dado sensível bruto) ou limite do destino.
  :::
- **P:** "Toda hora aparece uma arquitetura nova. Como você decide qual usar?"
  :::{dropdown} Resposta modelo
  Não sigo o hype; parto do problema e do trade-off. Que dados tenho (estruturados ou variados)? Que latência o negócio exige (batch ou streaming)? Qual o orçamento? A partir daí escolho a mais simples que atende — hoje, quase sempre um lakehouse com ELT — e adiciono complexidade (streaming, data mesh) só quando a escala ou a organização justificam.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Armbrust et al. — Lakehouse** (a convergência lake + warehouse).
- **Reis & Housley — Fundamentals of Data Engineering** (mapa das arquiteturas e ETL/ELT).
- **Dehghani — Data Mesh Principles** (a virada organizacional).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — arquiteturas e ETL/ELT. <!-- @reis2022 -->
- Armbrust, M. et al. *Lakehouse: A New Generation of Open Platforms* (2021) — lakehouse. <!-- @armbrust2020 -->
- Dehghani, Z. *Data Mesh Principles and Logical Architecture* (2020) — data mesh. <!-- @dehghani2020 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
