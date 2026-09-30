# Spark avançado: plano de execução, skew e otimização

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Seu job Spark processa 1 TB em 40 minutos, e você percebe que **199 tarefas terminam em 30 segundos e
1 tarefa leva 38 minutos**. Ou: um join entre uma tabela gigante e uma pequena está **arrastando as
duas pela rede** quando poderia ser instantâneo. Ou o job **relê o mesmo DataFrame cinco vezes** porque
você esqueceu de cachear. Esses são os problemas que fazem Spark ser lento — e nenhum se resolve com
"mais máquinas", só entendendo **como o Spark executa** e onde estão os gargalos: **shuffle**, **data
skew** e a **estratégia de join**. Você viu partições e shuffle por alto (teoria 03); aqui está a
mecânica de execução e tuning que a FIAP e vagas de Big Data cobram.

## 💡 Conceito (o porquê)

### Como o Spark executa: lazy, Catalyst, stages
Transformações no Spark são **lazy**: nada roda até uma **ação** (`count`, `write`, `collect`). Ao
disparar, o **Catalyst** (otimizador) reescreve seu plano (predicate pushdown, column pruning, reordem
de operações) e gera um plano físico; o **Tungsten** otimiza memória/CPU. Esse plano é dividido em:
- **Job** (por ação) → **stages** → **tasks** (uma por partição).
A fronteira entre stages é sempre um **shuffle**. Ler o **plano de execução** (`.explain()`) é como você
descobre onde está o custo.

### Narrow vs wide: o divisor de águas é o shuffle
- **Transformações narrow** (`map`, `filter`, `select`): cada partição de saída depende de **uma**
  partição de entrada. Ficam no **mesmo stage**, sem rede — baratas.
- **Transformações wide** (`groupBy`, `join`, `distinct`, `repartition`): a saída depende de **várias**
  partições, exigindo **shuffle** (redistribuir dados pela rede entre executores). Cada wide **fecha um
  stage e abre outro**, e é a operação **mais cara** do Spark.

Regra prática: o número de stages ≈ número de shuffles + 1. **Menos shuffle = mais rápido.** Filtrar e
projetar cedo (antes dos joins/aggs) reduz o volume que vai para o shuffle.

### Data skew: a partição que atrasa tudo
Um stage só termina quando sua **tarefa mais lenta** termina. Se uma chave é muito mais frequente que
as outras (ex.: 40% dos eventos têm `cliente_id = NULL` ou um cliente gigante), o shuffle joga tudo dela
numa **única partição** — uma tarefa processa 40% dos dados enquanto as outras ficam ociosas. Isso é
**data skew**, a causa nº 1 de "1 tarefa de 38 minutos". Defesas:
- **Salting:** adicionar um sufixo aleatório à chave problemática para espalhá-la em várias partições
  (e reagrupar depois).
- **AQE (Adaptive Query Execution):** o Spark moderno detecta partições skewed em runtime e as
  **divide** automaticamente (skew join optimization) — ligue o AQE.
- Filtrar/tratar a chave problemática (ex.: NULLs) separadamente.

### Estratégias de join: broadcast vs sort-merge
- **Broadcast join:** se uma das tabelas é **pequena** (cabe na memória do executor), o Spark a
  **replica** para todos os nós e faz o join **sem shuffle** da tabela grande — ordens de grandeza mais
  rápido. Acontece automaticamente abaixo de um limite (`autoBroadcastJoinThreshold`), ou via
  `broadcast(df)`.
- **Sort-merge / shuffle hash join:** quando as duas são grandes, ambas são **shuffled** e unidas — caro,
  mas inevitável para grande×grande.

Escolher (ou deixar o Catalyst escolher, com estatísticas boas) broadcast quando cabível é uma das
maiores alavancas de performance. O erro comum é um grande×pequeno virar sort-merge por falta de
estatística/limite.

### Caching e persistência
Um DataFrame reusado em **várias ações** é recomputado do zero a cada uma (lazy). `cache()`/`persist()`
materializam o resultado (em memória, ou memória+disco) para reuso — essencial em pipelines iterativos
(ML) e quando o mesmo intermediário alimenta várias saídas. O custo é memória; cacheie o que é **reusado
e caro de recomputar**, e libere (`unpersist`) quando não precisar mais.

### Dimensionar partições: nem grandes demais, nem pequenas demais
O paralelismo é o número de partições. **Poucas e grandes** → subutiliza o cluster e arrisca spill/OOM;
**muitas e minúsculas** → overhead de agendamento domina. Alvo típico: partições de ~100–200 MB.
`repartition(n)` faz shuffle para rebalancear (caro, mas espalha uniforme); `coalesce(n)` **reduz** sem
shuffle (barato, mas pode desbalancear) — usado antes de gravar para não gerar milhares de arquivinhos.
O **AQE** também ajusta o número de partições do shuffle em runtime (coalesce automático).

## 🔎 Exemplo
Um job junta `eventos` (1 TB) com `dim_cliente` (50 MB) e agrega por cliente, levando 40 min por causa
de uma tarefa travada. O `.explain()` revela: (1) o join virou **sort-merge** (as duas shuffled) — força
**broadcast** da `dim_cliente` (50 MB cabe), eliminando o shuffle da tabela grande; (2) há **skew** no
`groupBy` porque 40% dos eventos têm `cliente_id` nulo — trata-se o NULL à parte e **liga o AQE** (skew
optimization divide a partição gigante); (3) o DataFrame de eventos filtrado é reusado em duas saídas —
um **`cache()`** evita relê-lo. Resultado: 40 min → 4 min, sem adicionar uma máquina — só removendo
shuffle, skew e recomputação.

:::{admonition} 📖 Da literatura
:class: seealso
Armbrust et al., no paper do Spark SQL, descrevem o **otimizador Catalyst** (plano lógico → otimizado →
físico); Dean & Ghemawat estabelecem o modelo de shuffle/partição do MapReduce que o Spark herda e
otimiza. Kleppmann cobre processamento batch distribuído e o custo do shuffle. — *Spark SQL: Relational Data
Processing in Spark*; *MapReduce*; *Designing Data-Intensive Applications* (cap. 10).
:::

:::{admonition} 🏭 Do mundo real
:class: important
A tríade de tuning de Spark em produção é: **reduzir shuffle** (filtrar/projetar cedo, broadcast joins),
**tratar skew** (salting/AQE) e **cachear o reusado**. "Adicionar executores" quase nunca resolve um job
lento por skew ou por sort-merge desnecessário — é preciso ler o plano. Ligar o **AQE** resolve boa parte
do skew e do dimensionamento de partições automaticamente. — Documentação do Spark (Performance Tuning/AQE).
:::

## ⚠️ Erros comuns
- **Ignorar o `.explain()`** — otimizar no escuro; o plano mostra shuffles, join strategy e skew.
- **Grande×pequeno virando sort-merge** — deveria ser **broadcast** do lado pequeno.
- **Data skew não tratado** — uma tarefa segura o stage inteiro; use salting/AQE.
- **Recomputar DataFrame reusado** — sem `cache()`, cada ação relê tudo.
- **Partições mal dimensionadas** — grandes demais (spill/OOM) ou pequenas demais (overhead); mire ~100–200 MB.

## 💼 O que o mercado espera
Ler um plano de execução, distinguir narrow×wide (e localizar shuffles), aplicar **broadcast join**,
diagnosticar e corrigir **data skew** (salting/AQE), usar **cache** com critério e dimensionar partições
(repartition/coalesce). É o núcleo de tuning de Spark — assunto certo em entrevista de Big Data.

:::{admonition} ✨ Em resumo
:class: resumo
- Execução **lazy** + **Catalyst**: job → **stages** (fronteira = **shuffle**) → tasks (uma por partição).
- **Narrow** (map/filter, sem rede) vs **wide** (groupBy/join, **shuffle** — o mais caro); menos shuffle = mais rápido.
- **Data skew**: uma chave dominante trava o stage → **salting** ou **AQE** (skew optimization).
- **Broadcast join** (lado pequeno replicado, sem shuffle) > sort-merge quando cabível; **cache** o reusado; partições ~100–200 MB (repartition/coalesce/AQE).
:::

## 🧠 Quiz de recall
1. O que define a fronteira entre stages no Spark?
   :::{dropdown} Resposta
   O shuffle: transformações wide (groupBy, join, distinct, repartition) exigem redistribuir dados pela rede e fecham um stage/abrem outro. Nº de stages ≈ nº de shuffles + 1.
   :::
2. Qual a diferença entre narrow e wide, e por que importa?
   :::{dropdown} Resposta
   Narrow: cada partição de saída vem de uma de entrada (map/filter), sem rede, mesmo stage — barato. Wide: saída depende de várias partições, exige shuffle — caro. Reduzir wides/shuffle é a chave da performance.
   :::
3. O que é data skew e como tratá-lo?
   :::{dropdown} Resposta
   Uma chave muito frequente concentra dados numa partição, e uma tarefa lenta segura o stage inteiro. Trata-se com salting (espalhar a chave), AQE (skew optimization automática) ou tratando a chave problemática à parte.
   :::
4. Quando o Spark usa broadcast join e por que é rápido?
   :::{dropdown} Resposta
   Quando uma tabela é pequena o bastante para caber na memória do executor: o Spark a replica a todos os nós e junta sem shuffle da tabela grande — muito mais rápido que sort-merge (que shuffla as duas).
   :::
5. Quando cachear um DataFrame?
   :::{dropdown} Resposta
   Quando ele é reusado em várias ações e é caro de recomputar (execução lazy recomputa do zero a cada ação); cache()/persist() materializam para reuso, ao custo de memória.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Um job Spark tem 199 tarefas rápidas e 1 tarefa que leva 30 minutos. O que é e como resolve?"
  :::{dropdown} Resposta modelo
  É data skew: uma chave dominante (às vezes NULL ou um cliente gigante) concentra os dados numa partição após o shuffle, e essa tarefa segura o stage. Diagnostico pelo plano/UI, e trato com salting (adicionar sufixo à chave para espalhar e reagrupar), ligando o AQE (skew join optimization divide a partição em runtime) e tratando a chave problemática separadamente. "Mais executores" não resolveria — o gargalo é uma única partição.
  :::
- **P:** "Um join entre uma tabela de 1 TB e uma de 40 MB está lento. O que você faz?"
  :::{dropdown} Resposta modelo
  Forço broadcast do lado pequeno: 40 MB cabe na memória do executor, então o Spark o replica a todos os nós e faz o join sem shuffle da tabela de 1 TB — em vez de sort-merge, que shufflaria as duas. Confirmo no `.explain()` que virou BroadcastHashJoin; se não virou sozinho, uso `broadcast(df_pequeno)` ou ajusto o autoBroadcastJoinThreshold. É uma das maiores alavancas de performance em Spark.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Armbrust et al. — Spark SQL: Relational Data Processing in Spark** (o otimizador Catalyst).
- **Kleppmann — Designing Data-Intensive Applications** (cap. 10, batch e shuffle).
- **Documentação do Spark** — SQL performance tuning, AQE, join strategies.

## 📚 Referências
- Armbrust, M. et al. *Spark SQL: Relational Data Processing in Spark* (2015) — otimizador Catalyst. <!-- @armbrust2015 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — batch distribuído e shuffle. <!-- @kleppmann2017 -->
- Dean, J.; Ghemawat, S. *MapReduce: Simplified Data Processing on Large Clusters* (2004) — modelo de partição/shuffle. <!-- @dean2004 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
