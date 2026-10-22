# Processamento distribuído e a arquitetura do Spark

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Até aqui, seus dados cabem numa máquina (Postgres, DuckDB, pandas). Mas e quando são
**terabytes** — grandes demais para a memória de um servidor? A resposta é **processamento
distribuído**: dividir o trabalho entre **muitas máquinas**. O **Apache Spark** é o motor
dominante para isso em dados. Esta unidade explica de onde veio (MapReduce) e como o Spark se
organiza (driver/executors, RDD vs DataFrame, *lazy evaluation*) — a base para usá-lo bem.

## 💡 Conceito (o porquê)

### De MapReduce ao Spark
O **MapReduce** (Google, 2004) provou que dá para processar dados massivos dividindo em
**map** (transforma pedaços em paralelo) e **reduce** (agrega), com tolerância a falhas. Mas
ele escreve em disco a cada etapa — lento para pipelines com muitos passos. O **Spark**
manteve a ideia (dividir + tolerar falhas) mas processa **em memória** e encadeia operações,
ficando ordens de grandeza mais rápido.

### Arquitetura: driver e executors
Um job Spark tem:
- **Driver:** o "cérebro" — roda seu código, monta o plano e coordena.
- **Executors:** os "trabalhadores" — rodam as tarefas em paralelo, cada um sobre uma fatia dos dados.
- **Cluster manager:** distribui recursos (YARN, Kubernetes, standalone).

Os dados são divididos em **partições**; cada executor processa partições em paralelo. Mais
partições/executors = mais paralelismo.

### RDD vs DataFrame
- **RDD** (Resilient Distributed Dataset): a API de baixo nível (coleção distribuída, tolerante
  a falhas). Poderosa, mas "crua".
- **DataFrame:** a API de alto nível (tabela distribuída com colunas/tipos). É a recomendada:
  mais legível e **otimizada** pelo motor (**Catalyst**), que reescreve seu plano para rodar
  melhor. Prefira DataFrame/SQL a RDD no dia a dia.

### Lazy evaluation: transformações vs ações
Operações Spark são de dois tipos:
- **Transformações** (`select`, `filter`, `groupBy`, `join`): **lazy** — não executam na hora,
  só **montam o plano** (um DAG).
- **Ações** (`count`, `collect`, `show`, `write`): **disparam** a execução de todo o plano acumulado.

Ser lazy deixa o Catalyst **otimizar o plano inteiro** antes de rodar (ex.: empurrar filtros
para o início, ler menos dados). Nada acontece até uma **ação**.

## 🔎 Exemplo
`df.filter(ano==2025).groupBy("categoria").sum("valor")` — nada roda ainda (só transformações).
Ao chamar `.show()` (ação), o Spark otimiza (empurra o filtro de ano para a leitura), distribui
as partições entre os executors, cada um agrega a sua parte, e o resultado é combinado. Se
fossem TBs, isso rodaria em paralelo em dezenas de máquinas — inviável numa só.

**Rodando de verdade** (🐳 bancada, Spark 3.5): o exemplo acima, com o plano impresso **antes** da ação.

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("lazy").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# 1) dados em Parquet: 3 anos de vendas
(spark.range(300_000)
      .select((2023 + F.col("id") % 3).alias("ano"),
              F.element_at(F.array(F.lit("livros"), F.lit("casa"), F.lit("moda")), (F.floor(F.col("id") / 3) % 3 + 1).cast("int")).alias("categoria"),
              (F.col("id") % 100).alias("valor"))
      .write.mode("overwrite").parquet("/tmp/vendas"))

# 2) transformações: NADA roda aqui, o Spark só monta o plano
df = (spark.read.parquet("/tmp/vendas")
           .filter(F.col("ano") == 2025)
           .groupBy("categoria").agg(F.sum("valor").alias("receita")))

# 3) o plano físico, antes de executar
df.explain()

# 4) a ação dispara o job
df.orderBy("categoria").show()
```

Salve o código como `exemplo.py` na raiz do repositório (no container ela é `/work`) e rode:

```bash
cd ambiente
docker compose --profile spark run --rm spark /opt/spark/bin/spark-submit /work/exemplo.py
```

Saída:

```text
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- HashAggregate(keys=[categoria#12], functions=[sum(valor#13L)])
   +- Exchange hashpartitioning(categoria#12, 200), ENSURE_REQUIREMENTS, [plan_id=34]
      +- HashAggregate(keys=[categoria#12], functions=[partial_sum(valor#13L)])
         +- Project [categoria#12, valor#13L]
            +- Filter (isnotnull(ano#11L) AND (ano#11L = 2025))
               +- FileScan parquet [ano#11L,categoria#12,valor#13L] Batched: true, DataFilters: [isnotnull(ano#11L), (ano#11L = 2025)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[file:/tmp/vendas], PartitionFilters: [], PushedFilters: [IsNotNull(ano), EqualTo(ano,2025)], ReadSchema: struct<ano:bigint,categoria:string,valor:bigint>


+---------+-------+
|categoria|receita|
+---------+-------+
|     casa|1649967|
|   livros|1649967|
|     moda|1650066|
+---------+-------+
```

Leia o plano de baixo para cima. O `FileScan` já traz `PushedFilters: [... EqualTo(ano,2025)]`: o otimizador empurrou o filtro para a leitura do Parquet, como o texto descreve. O `HashAggregate` aparece duas vezes, com o `Exchange` no meio: cada executor soma a sua parte (`partial_sum`), o shuffle reúne as categorias e a soma final fecha a conta. Até o `.show()` nenhum dado foi lido; o `explain()` só mostrou o plano.

:::{admonition} 📖 Da literatura
:class: seealso
Dean & Ghemawat introduziram o **MapReduce** como modelo para processar grandes volumes em
clusters com tolerância a falhas; o Spark é a evolução que mantém isso mas processa em memória
e otimiza o plano. Kleppmann situa ambos no processamento **batch** distribuído. — *MapReduce*
(2004); *Designing Data-Intensive Applications*, cap. 10.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A documentação do Spark recomenda a **API de DataFrame** (otimizada pelo Catalyst) sobre RDDs
para a maioria dos casos, e a *lazy evaluation* é o que permite ao motor reordenar/otimizar o
trabalho antes de tocar nos dados. — Apache Spark, documentação oficial.
:::

## ⚠️ Erros comuns
- Usar **Spark para dados pequenos** — o overhead de distribuir não compensa; use pandas/DuckDB/SQL.
- Preferir **RDD** quando DataFrame resolve — perde a otimização do Catalyst.
- Esquecer que transformações são **lazy** — "meu código não roda" (falta uma ação).
- `collect()` num DataFrame gigante — traz tudo para o driver e estoura a memória.
- Ignorar partições — poucas = sem paralelismo; muitas = overhead.

## 💼 O que o mercado espera
Entender quando (e quando **não**) usar Spark, a diferença DataFrame vs RDD e o modelo lazy é
esperado. "Por que meu job Spark não fez nada até o `.show()`?" e "driver vs executor" são
perguntas de entrevista.

:::{admonition} ✨ Em resumo
:class: resumo
- Processamento **distribuído** divide o trabalho entre máquinas; Spark evolui o MapReduce processando **em memória**.
- Arquitetura: **driver** (coordena) + **executors** (processam partições em paralelo).
- **DataFrame** (alto nível, otimizado pelo Catalyst) > RDD na maioria dos casos.
- **Transformações são lazy** (montam o DAG); só uma **ação** dispara a execução.
:::

## 🧠 Quiz de recall
1. O que o Spark melhorou em relação ao MapReduce?
   :::{dropdown} Resposta
   Manteve dividir+tolerar falhas, mas processa em memória e encadeia operações (sem escrever em disco a cada etapa), ficando muito mais rápido para pipelines multi-passo.
   :::
2. Qual o papel do driver e dos executors?
   :::{dropdown} Resposta
   O driver roda seu código, monta o plano e coordena; os executors executam as tarefas em paralelo, cada um sobre partições dos dados.
   :::
3. RDD vs DataFrame — qual preferir e por quê?
   :::{dropdown} Resposta
   DataFrame: API de alto nível com colunas/tipos, otimizada pelo Catalyst (mais legível e rápida). RDD é baixo nível; use só quando precisar de controle fino.
   :::
4. Diferença entre transformação e ação?
   :::{dropdown} Resposta
   Transformações (select/filter/groupBy) são lazy — montam o plano (DAG); ações (count/show/write) disparam a execução do plano.
   :::
5. Por que `collect()` num DataFrame enorme é perigoso?
   :::{dropdown} Resposta
   Traz todos os dados dos executors para a memória do driver, podendo estourá-la; use ações que não materializam tudo (write, agregações) ou limite os dados.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Quando você NÃO usaria Spark?"
  :::{dropdown} Resposta modelo
  Quando os dados cabem numa máquina: o overhead de distribuir (JVM, shuffle, coordenação) não compensa. Aí pandas/DuckDB/SQL num Postgres são mais simples e rápidos. Spark brilha em volumes que não cabem em um nó.
  :::
- **P:** "Por que meu job Spark não executou nada até o `.show()`?"
  :::{dropdown} Resposta modelo
  Porque transformações são lazy — só montam o plano (DAG). A execução só dispara numa ação como `show`, `count`, `collect` ou `write`. Isso permite ao Catalyst otimizar o plano inteiro antes de rodar.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Apache Spark docs** — *Overview*, *RDD vs DataFrame*, *Cluster mode*.
- **Kleppmann — Designing Data-Intensive Applications**, cap. 10 (batch/MapReduce/dataflow).
- **Dean & Ghemawat — MapReduce** (2004), o paper fundador.

## 📚 Referências
- Apache Spark — Documentação oficial (arquitetura, DataFrame, lazy evaluation). <!-- @docs-spark -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 10 (batch distribuído). <!-- @kleppmann2017 -->
- Dean, J.; Ghemawat, S. *MapReduce: Simplified Data Processing on Large Clusters* (2004) — modelo de processamento distribuído. <!-- @dean2004 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-10-21
