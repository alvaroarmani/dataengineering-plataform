# Partições, shuffle e otimização no Spark

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Dois jobs Spark com a "mesma" lógica podem ter desempenho absurdamente diferente. O que separa
um job rápido de um lento (e caro) quase sempre é uma coisa: o **shuffle** — a movimentação de
dados entre executors. Entender **partições** e **shuffle** é o que te faz otimizar Spark de
verdade (e é a pergunta técnica mais comum sobre Spark em entrevistas).

## 💡 Conceito (o porquê)

### Partições: a unidade de paralelismo
Um DataFrame é dividido em **partições**; cada executor processa uma por vez. Paralelismo =
quantas partições rodam ao mesmo tempo. **Poucas** partições → executors ociosos (subutiliza).
**Muitas** partições minúsculas → overhead de agendamento. O ideal é um meio-termo (partições
nem gigantes nem minúsculas).

### Transformações narrow vs wide
- **Narrow:** cada partição de saída depende de **uma** partição de entrada (`filter`, `select`,
  `withColumn`). Rodam **localmente**, sem mover dados — baratas.
- **Wide:** a saída depende de **várias** partições de entrada (`groupBy`, `join`, `distinct`,
  `orderBy`). Exigem **shuffle** — caras.

### Shuffle: o gargalo
O **shuffle** redistribui os dados pela rede para agrupar chaves iguais no mesmo executor (para
um `groupBy`/`join`). Envolve **rede + disco + serialização** — é a operação mais cara do Spark.
Não dá para eliminar (agregações precisam), mas dá para **reduzir**:
- **Filtrar cedo** (menos dados para embaralhar).
- **Selecionar só as colunas necessárias**.
- Em joins com uma tabela **pequena**, usar **broadcast join** (manda a pequena inteira para
  todos os executors, evitando shuffle da grande).
- Evitar `orderBy` global desnecessário.

### Skew (dados desbalanceados)
Se uma chave concentra muito volume (ex.: 90% dos eventos são de um cliente), uma partição fica
gigante e segura o job inteiro — **data skew**. Sinais: uma task muito mais lenta que as outras.
Mitiga-se com técnicas como *salting* ou o *skew join* do Spark.

### Otimizações que o Spark já faz (Catalyst/AQE)
O **Catalyst** otimiza o plano (empurra filtros, remove colunas). O **AQE** (Adaptive Query
Execution) ajusta em tempo de execução (ex.: coalescer partições pequenas, tratar skew). Você
ajuda dando um bom plano (filtrar cedo, tipos certos, formatos colunares).

## 🔎 Exemplo
`grande.join(pequena, "id").groupBy("cat").sum("v")`: o `join` e o `groupBy` são **wide** →
shuffle. Se `pequena` cabe na memória, um **broadcast join** evita embaralhar a `grande`
(economia enorme). Filtrar a `grande` **antes** do join reduz o que é embaralhado. `filter`
sozinho seria narrow (sem shuffle).

**Rodando de verdade** (🐳 bancada, Spark 3.5): o mesmo join planejado duas vezes, com e sem broadcast.

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("joins").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

grande  = spark.range(1_000_000).select((F.col("id") % 1000).alias("id"), (F.col("id") % 7).alias("v"))
pequena = spark.range(1000).select(F.col("id"), (F.col("id") % 10).cast("string").alias("cat"))

def consulta():
    return grande.join(pequena, "id").groupBy("cat").agg(F.sum("v").alias("total"))

consulta().explain()       # padrão: a pequena cabe no limite de broadcast (10 MB)

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)   # desliga o broadcast automático
consulta().explain()       # agora as duas tabelas são embaralhadas

# para forçar o broadcast mesmo acima do limite: grande.join(F.broadcast(pequena), "id")
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
+- HashAggregate(keys=[cat#8], functions=[sum(v#3L)])
   +- Exchange hashpartitioning(cat#8, 200), ENSURE_REQUIREMENTS, [plan_id=40]
      +- HashAggregate(keys=[cat#8], functions=[partial_sum(v#3L)])
         +- Project [v#3L, cat#8]
            +- BroadcastHashJoin [id#2L], [id#6L], Inner, BuildRight, false
               :- Project [(id#0L % 1000) AS id#2L, (id#0L % 7) AS v#3L]
               :  +- Filter isnotnull((id#0L % 1000))
               :     +- Range (0, 1000000, step=1, splits=12)
               +- BroadcastExchange HashedRelationBroadcastMode(List(input[0, bigint, false]),false), [plan_id=35]
                  +- Project [id#6L, cast((id#6L % 10) as string) AS cat#8]
                     +- Range (0, 1000, step=1, splits=12)


== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- HashAggregate(keys=[cat#8], functions=[sum(v#3L)])
   +- Exchange hashpartitioning(cat#8, 200), ENSURE_REQUIREMENTS, [plan_id=86]
      +- HashAggregate(keys=[cat#8], functions=[partial_sum(v#3L)])
         +- Project [v#3L, cat#8]
            +- SortMergeJoin [id#2L], [id#6L], Inner
               :- Sort [id#2L ASC NULLS FIRST], false, 0
               :  +- Exchange hashpartitioning(id#2L, 200), ENSURE_REQUIREMENTS, [plan_id=78]
               :     +- Project [(id#0L % 1000) AS id#2L, (id#0L % 7) AS v#3L]
               :        +- Filter isnotnull((id#0L % 1000))
               :           +- Range (0, 1000000, step=1, splits=12)
               +- Sort [id#6L ASC NULLS FIRST], false, 0
                  +- Exchange hashpartitioning(id#6L, 200), ENSURE_REQUIREMENTS, [plan_id=79]
                     +- Project [id#6L, cast((id#6L % 10) as string) AS cat#8]
                        +- Range (0, 1000, step=1, splits=12)
```

No primeiro plano há **um** `Exchange` (o do `groupBy`) e o join é `BroadcastHashJoin`: a pequena foi copiada inteira para cada executor e a grande ficou onde estava. No segundo, o join virou `SortMergeJoin` e ganhou **dois** `Exchange hashpartitioning(id...)` a mais: as duas tabelas atravessam a rede para que as chaves iguais se encontrem. Contar os `Exchange` do plano é o jeito mais rápido de achar o custo de um job.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann descreve o custo do **particionamento e da redistribuição (shuffle)** em
processamento distribuído — mover dados pela rede para juntar chaves é o principal gargalo, e
reduzir esse tráfego (filtrar cedo, broadcast de tabelas pequenas) é a essência da otimização.
— *Designing Data-Intensive Applications*, cap. 10.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A documentação do Spark recomenda **broadcast joins** para tabelas pequenas, filtrar/projetar
cedo, e usar o **AQE** para coalescer partições e tratar skew automaticamente — as alavancas
que mais impactam desempenho e custo. — Apache Spark, documentação oficial.
:::

## ⚠️ Erros comuns
- Não reparar que `groupBy`/`join`/`distinct` causam **shuffle** — o job fica lento sem explicação.
- **Join de uma tabela pequena sem broadcast** — embaralha a grande à toa.
- Filtrar **depois** do join/agregação em vez de **antes** — embaralha dados que seriam descartados.
- Ignorar **skew** — uma partição gigante trava o job.
- Partições demais/de menos — overhead ou subutilização.

## 💼 O que o mercado espera
"O que é shuffle e como reduzi-lo?" é **a** pergunta de Spark em entrevista. Saber narrow vs
wide, broadcast join e filtrar cedo — e ler o `explain()` — é o que caracteriza quem sabe operar
Spark, não só escrever.

:::{admonition} ✨ Em resumo
:class: resumo
- **Partições** = unidade de paralelismo (nem gigantes, nem minúsculas).
- **Narrow** (filter/select) não move dados; **wide** (groupBy/join/distinct/orderBy) causa **shuffle** (caro).
- Reduza shuffle: **filtrar/projetar cedo**, **broadcast join** para tabelas pequenas, evitar orderBy global.
- **Skew** (chave concentrada) trava o job; Catalyst/**AQE** otimizam parte automaticamente.
:::

## 🧠 Quiz de recall
1. O que é uma partição e como afeta o paralelismo?
   :::{dropdown} Resposta
   É a unidade de dados que um executor processa por vez; o paralelismo é quantas partições rodam simultaneamente. Poucas subutilizam; muitas minúsculas geram overhead.
   :::
2. Narrow vs wide transformation?
   :::{dropdown} Resposta
   Narrow: saída depende de uma partição de entrada (filter/select) — sem mover dados. Wide: depende de várias (groupBy/join/distinct/orderBy) — exige shuffle.
   :::
3. O que é shuffle e por que é caro?
   :::{dropdown} Resposta
   Redistribuir dados pela rede para agrupar chaves iguais no mesmo executor (para groupBy/join). Envolve rede, disco e serialização — a operação mais cara.
   :::
4. Como reduzir shuffle?
   :::{dropdown} Resposta
   Filtrar e selecionar colunas cedo, usar broadcast join para tabelas pequenas, evitar orderBy global desnecessário; deixar o AQE coalescer/ tratar skew.
   :::
5. O que é data skew?
   :::{dropdown} Resposta
   Distribuição desbalanceada de uma chave (uma partição fica gigante), fazendo uma task travar o job; mitiga-se com salting/skew join.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "O que é shuffle e como você o reduz?"
  :::{dropdown} Resposta modelo
  É a redistribuição de dados pela rede para juntar chaves (groupBy/join) — o gargalo do Spark. Reduzo filtrando e projetando cedo (menos dados a embaralhar), usando broadcast join quando uma tabela cabe na memória, evitando orderBy global e deixando o AQE coalescer partições/tratar skew.
  :::
- **P:** "Uma task está muito mais lenta que as outras. O que é?"
  :::{dropdown} Resposta modelo
  Provável data skew: uma chave concentra volume e sua partição fica gigante. Mitigo com salting da chave, o skew join do Spark, ou repartição — e confirmo pelo Spark UI (task com muito mais dados/tempo).
  :::

## 🚀 Para ir além (leitura dirigida)
- **Apache Spark docs** — *Performance tuning*, *Broadcast joins*, *Adaptive Query Execution*.
- **Kleppmann — Designing Data-Intensive Applications**, cap. 10 (partição, shuffle, joins distribuídos).

## 📚 Referências
- Apache Spark — Documentação oficial (tuning, shuffle, broadcast, AQE). <!-- @docs-spark -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 10 (shuffle, joins distribuídos). <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — desempenho e custo em escala. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-10-21
