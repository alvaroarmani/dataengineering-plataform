# PySpark: DataFrames, transformações e ações

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Sabendo a arquitetura (U1), agora você **escreve** Spark. A boa notícia para quem veio do
pandas/SQL (M3/M4): a API de **DataFrame** do PySpark é muito parecida — `select`, `filter`,
`groupBy`, `join`, `withColumn`. A diferença é que roda **distribuído** e é **lazy**. Esta
unidade é o "mão na massa" do Spark.

## 💡 Conceito (o porquê)

### Criar e ler DataFrames
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("curso").getOrCreate()
df = spark.read.parquet("s3a://dados/vendas/")     # ou .csv(..., header=True)
```
O Spark lê **em paralelo**; formatos colunares (Parquet, M8) permitem ler só as colunas usadas.

### Transformações comuns (parecem SQL/pandas)
```python
from pyspark.sql import functions as F
(df.filter(F.col("ano") == 2025)
   .withColumn("receita", F.col("preco") * F.col("qtd"))
   .groupBy("categoria")
   .agg(F.sum("receita").alias("total"))
   .orderBy(F.col("total").desc()))
```
- `select`, `filter`/`where`, `withColumn` (nova coluna), `groupBy().agg()`, `join`, `orderBy`.
- Use **`F.col`** e as funções de `pyspark.sql.functions` (não funções Python puras em colunas).

### Ações disparam o trabalho
`show()`, `count()`, `collect()` (cuidado!), `write` — só aí o plano roda. `df.explain()` mostra
o plano físico (útil para entender o que o Catalyst fez).

### Escrever (particionado)
```python
(df.write.mode("overwrite")
   .partitionBy("ano")            # grava uma pasta por ano (pruning na leitura)
   .parquet("s3a://dados/vendas_out/"))
```
`partitionBy` no destino é o análogo do particionamento do M6 — acelera leituras filtradas.

### Spark SQL: a mesma coisa em SQL
```python
df.createOrReplaceTempView("vendas")
spark.sql("SELECT categoria, SUM(preco*qtd) t FROM vendas WHERE ano=2025 GROUP BY categoria")
```
DataFrame e SQL são **equivalentes** (mesmo otimizador) — use o que for mais claro.

## 🔎 Exemplo
Ler o NYC Taxi (Parquet, M8) de um bucket, filtrar um mês, calcular receita por dia e gravar
particionado por dia. Como é lazy + colunar, o Spark lê só as colunas necessárias e distribui o
cálculo — o mesmo código roda para 1 GB ou 1 TB, mudando só o tamanho do cluster.

:::{admonition} 📖 Da literatura
:class: seealso
A documentação do Spark apresenta a API de DataFrame como o jeito idiomático (equivalente ao
Spark SQL, mesmo otimizador), com `pyspark.sql.functions` para operações de coluna — uma ponte
natural para quem já usa pandas/SQL. — Apache Spark, documentação oficial.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Times escrevem a maior parte do Spark em DataFrame/SQL (legível e otimizado), reservando RDD
para casos raros. Gravar **particionado** por data no data lake é padrão para baratear leituras
a jusante. — Apache Spark, docs oficiais.
:::

## ⚠️ Erros comuns
- Aplicar **funções Python puras** em colunas em vez de `F.` — perde otimização/vetorização (ou nem funciona distribuído).
- `collect()` para "ver os dados" num DF enorme — use `show(n)` ou `limit`.
- Não **particionar** a escrita — leituras futuras varrem tudo.
- Achar que `withColumn` muda o DF original — DataFrames são **imutáveis**; ele retorna um novo.
- Esquecer a **ação** — o pipeline "não roda".

## 💼 O que o mercado espera
Escrever transformações em PySpark (filter/groupBy/join/withColumn), usar `F.`, gravar
particionado e alternar com Spark SQL é o trabalho diário em times que usam Spark. A semelhança
com pandas/SQL acelera — mas saber que é lazy/distribuído é o diferencial.

:::{admonition} ✨ Em resumo
:class: resumo
- A API de **DataFrame** do PySpark lembra pandas/SQL: `select/filter/withColumn/groupBy/join`.
- Use **`F.col`** e `pyspark.sql.functions`; DataFrames são **imutáveis** (retornam novos).
- **Ações** (`show`, `count`, `write`) disparam; `explain()` mostra o plano.
- Grave **particionado** (`partitionBy`) e alterne com **Spark SQL** (equivalente).
:::

## 🧠 Quiz de recall
1. Cite quatro transformações comuns de DataFrame.
   :::{dropdown} Resposta
   select, filter/where, withColumn (nova coluna), groupBy().agg(); também join e orderBy.
   :::
2. Por que usar `F.col`/`pyspark.sql.functions` em vez de funções Python puras?
   :::{dropdown} Resposta
   Porque elas operam nas colunas de forma distribuída e otimizável pelo Catalyst; funções Python puras não se traduzem no plano (ou exigem UDFs lentas).
   :::
3. `withColumn` altera o DataFrame original?
   :::{dropdown} Resposta
   Não — DataFrames são imutáveis; retorna um novo DataFrame com a coluna adicionada.
   :::
4. Para que serve `partitionBy` na escrita?
   :::{dropdown} Resposta
   Grava os dados em pastas por valor (ex.: por ano/dia), permitindo pruning nas leituras filtradas — mais rápido e barato.
   :::
5. DataFrame vs Spark SQL?
   :::{dropdown} Resposta
   São equivalentes (mesmo otimizador). Use o que for mais claro; dá para registrar uma view e consultar com spark.sql(...).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você escreveria uma agregação por categoria no PySpark?"
  :::{dropdown} Resposta modelo
  `df.filter(F.col("ano")==2025).groupBy("categoria").agg(F.sum(F.col("preco")*F.col("qtd")).alias("total")).orderBy(F.col("total").desc())` — e disparo com `.show()`. Ou o equivalente em Spark SQL após `createOrReplaceTempView`. Gravaria o resultado particionado por data.
  :::
- **P:** "Qual cuidado ao trazer resultados para o driver?"
  :::{dropdown} Resposta modelo
  Evitar `collect()` em DFs grandes (estoura a memória do driver). Uso `show(n)`/`limit`, ou escrevo o resultado no lake/warehouse em vez de materializar tudo no driver.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Apache Spark docs** — *DataFrame API*, *Functions*, *Data sources* (Parquet).
- **Reis & Housley — Fundamentals of Data Engineering** (processamento e transformação em escala).

## 📚 Referências
- Apache Spark — Documentação oficial (DataFrame API, functions, escrita particionada). <!-- @docs-spark -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — processamento em escala. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
