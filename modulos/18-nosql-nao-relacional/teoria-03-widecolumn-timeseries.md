# Wide-column (Cassandra) e bancos de série temporal

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Algumas cargas quebram qualquer banco em um único servidor: **milhões de escritas por segundo** de
sensores, cliques ou logs; dados que crescem para **terabytes** e precisam se espalhar por dezenas de
máquinas em vários data centers, sem gargalo e sem parar. E há um caso onipresente na engenharia de
dados moderna: **séries temporais** — métricas indexadas por tempo (uso de CPU, cotações, temperatura
de sensores) que chegam sem parar e são consultadas por intervalo. Esta unidade cobre as duas
famílias que atacam esses cenários: **wide-column** (Cassandra) e os **bancos de série temporal**.

## 💡 Conceito (o porquê)

### Wide-column (Cassandra): escala de escrita
Cassandra parece uma tabela, mas por baixo é um **mapa distribuído** particionado por chave. Suas
características centrais:
- **Sem servidor mestre** (masterless): todos os nós são iguais; não há um ponto único de gargalo ou
  falha. Escala **horizontalmente** — mais nós = mais capacidade, de forma linear.
- **Otimizado para escrita:** as gravações são pensadas para serem baratíssimas e distribuídas, o que
  o torna ideal para ingestão massiva (eventos, telemetria, feeds).
- **Alta disponibilidade** com replicação e consistência **ajustável** (você escolhe o nível por
  operação — o lado A do CAP, unidade 1).

### Chave de partição e chave de clustering
O coração da modelagem em Cassandra são duas chaves:
- **Partition key:** decide **em qual nó** a linha vive (`hash(partition key)`). Todas as linhas com a
  mesma partition key ficam **juntas** no mesmo nó — é o que dá acesso rápido e localidade.
- **Clustering key:** define a **ordem** das linhas **dentro** da partição (ex.: por timestamp
  decrescente), permitindo varrer um intervalo eficientemente.

### Modelagem pela consulta (query-first)
Aqui a regra da unidade 1 fica radical: em Cassandra você **modela a tabela para a consulta**, não os
dados para a "verdade". Não há JOIN nem consultas ad-hoc eficientes — então você desenha a partition
key e a clustering key **em torno da pergunta** que vai rodar, e **duplica** os dados em tabelas
diferentes se houver perguntas diferentes. Escolher a partition key errada gera *hotspots* (uma
partição gigante num nó) ou impossibilita a consulta.

### Bancos de série temporal
Uma **série temporal** é uma sequência de pontos `(tempo, valor)` — métricas, sensores, cotações.
Bancos especializados (InfluxDB, TimescaleDB, Prometheus) otimizam esse padrão:
- **Ingestão append-only** de alto volume, indexada por tempo.
- **Retenção e downsampling:** dados recentes em alta resolução; antigos **agregados** em janelas
  (média/máximo por minuto→hora→dia) e depois descartados — senão o volume é infinito.
- **Consultas por intervalo e por janela** (o "por minuto/hora" que você viu em streaming, M17).

Muitas vezes a série temporal é a **camada de serving** de um pipeline de streaming: os eventos do
Kafka (M17) são agregados por janela e gravados num TSDB que alimenta dashboards ao vivo.

### Como isso conecta com o resto do curso
Wide-column e time-series são frequentemente a **ponta de ingestão/serving em escala**: recebem o
firehose de eventos (o que o data warehouse batch não aguentaria em tempo real) e servem consultas
operacionais rápidas, enquanto o lake/warehouse (M06/M11) guarda o histórico para análise profunda.

## 🔎 Exemplo
Uma plataforma de IoT recebe leituras de milhões de sensores. As leituras entram numa tabela
**Cassandra** com **partition key = `sensor_id`** (todas as leituras de um sensor juntas num nó) e
**clustering key = `timestamp` decrescente** (as mais recentes primeiro) — assim "últimas N leituras
do sensor X" é uma consulta rápida numa partição. Em paralelo, as métricas agregadas por minuto vão
para um **banco de série temporal** com **downsampling** (minuto→hora após um dia) alimentando o
painel ao vivo. O histórico completo é despejado no data lake para análise. Escrita massiva no
wide-column, consulta temporal no TSDB, análise no lake — cada carga no banco certo.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann detalha **particionamento** (partition keys, hotspots, rebalanceamento) e **replicação**
como base da escala horizontal — exatamente os mecanismos que Cassandra explora — e discute o
armazenamento otimizado para escrita. — *Designing Data-Intensive Applications* (caps. 5 e 6).
:::

:::{admonition} 🏭 Do mundo real
:class: important
A decisão de projeto que mais dói em Cassandra é a **partition key**: escolhida errada, cria hotspots
(um nó sobrecarregado) ou partições gigantes que degradam tudo. Por isso se modela **pela consulta** e
se aceita **duplicar dados** em tabelas por pergunta — o oposto da normalização relacional. — prática
de mercado; Kleppmann.
:::

## ⚠️ Erros comuns
- **Partition key ruim** — gera hotspots (um nó sobrecarregado) ou partições grandes demais.
- **Esperar JOIN/consulta ad-hoc** em Cassandra — modele pela consulta e duplique tabelas.
- **Série temporal sem retenção/downsampling** — o volume cresce sem limite e o custo explode.
- **Usar um relacional único para escrita massiva de eventos** — vira gargalo; é caso de wide-column/TSDB.
- **Ignorar a clustering key** — sem ela, não há ordem/intervalo eficiente dentro da partição.

## 💼 O que o mercado espera
Saber que wide-column (Cassandra) é para escrita massiva e escala horizontal, modelar com
partition/clustering key **pela consulta**, e entender séries temporais (ingestão, retenção,
downsampling, consulta por janela). Aparece em system design de sistemas de alto volume/telemetria.

:::{admonition} ✨ Em resumo
:class: resumo
- **Wide-column (Cassandra)**: masterless, escala horizontal, otimizado para **escrita massiva**; consistência ajustável.
- **Partition key** decide o nó (localidade); **clustering key** ordena dentro da partição — modele **pela consulta** e duplique.
- **Série temporal**: pontos (tempo, valor); ingestão append-only, **retenção + downsampling**, consulta por intervalo/janela.
- Ambos são ponta de **ingestão/serving em escala**; o histórico profundo vive no lake/warehouse.
:::

## 🧠 Quiz de recall
1. Quais as características centrais do Cassandra?
   :::{dropdown} Resposta
   Masterless (sem mestre), escala horizontal linear, otimizado para escrita massiva, alta disponibilidade com consistência ajustável.
   :::
2. Qual a diferença entre partition key e clustering key?
   :::{dropdown} Resposta
   A partition key decide em qual nó a linha vive (localidade); a clustering key ordena as linhas dentro da partição (ex.: por tempo), permitindo varrer intervalos.
   :::
3. O que significa "modelar pela consulta" em Cassandra?
   :::{dropdown} Resposta
   Desenhar as chaves (e até duplicar dados em tabelas diferentes) em torno da pergunta que vai rodar, porque não há JOIN nem consulta ad-hoc eficiente.
   :::
4. O que é downsampling numa série temporal e por que importa?
   :::{dropdown} Resposta
   Agregar dados antigos em janelas maiores (minuto→hora→dia) e descartar a alta resolução; sem isso o volume cresce sem limite e o custo explode.
   :::
5. Por que um relacional único costuma falhar na escrita massiva de eventos?
   :::{dropdown} Resposta
   Porque concentra a escrita num servidor que vira gargalo; wide-column distribui a escrita por muitos nós sem mestre, escalando horizontalmente.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você armazenaria leituras de milhões de sensores para consultar 'últimas N por sensor'?"
  :::{dropdown} Resposta modelo
  Uma tabela wide-column (Cassandra) com partition key = sensor_id (todas as leituras do sensor juntas num nó) e clustering key = timestamp decrescente (mais recentes primeiro). Assim "últimas N do sensor X" é uma consulta rápida numa única partição. Para o painel agregado, mando métricas por minuto a um banco de série temporal com downsampling, e despejo o histórico no data lake.
  :::
- **P:** "Qual o maior risco ao modelar em Cassandra?"
  :::{dropdown} Resposta modelo
  A escolha da partition key. Se ela concentra escrita/leitura, cria hotspots (um nó sobrecarregado) ou partições gigantes que degradam o cluster. Por isso modelo pela consulta, distribuo bem as chaves e aceito duplicar dados em tabelas por pergunta, em vez de normalizar como no relacional.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (caps. 5 replicação, 6 particionamento).
- **Documentação do Apache Cassandra** — data modeling (partition/clustering keys).
- **Documentação do TimescaleDB / InfluxDB** — séries temporais, retenção e downsampling.

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — particionamento e replicação. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — armazenamento em escala. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — ingestão de alto volume. <!-- @densmore2021 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
