# Por que distribuir? Particionamento e falhas parciais

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você já usou Spark (M11), Kafka (M17) e Cassandra (M18) — todos **distribuídos**, rodando em vários
computadores ao mesmo tempo. Mas por quê? Um servidor moderno é potente; por que não colocar tudo
nele? Porque em algum ponto **um único computador não dá conta**: os dados não cabem no disco, as
consultas não cabem na memória, o volume de escrita passa do que uma máquina aguenta — e, se ela cai,
o sistema todo cai junto. A saída é **distribuir**: espalhar dados e trabalho por muitas máquinas.
Isso destrava escala quase ilimitada, mas abre uma caixa de problemas nova e traiçoeira — **falhas
parciais** — que está por baixo de toda ferramenta de dados em escala. Entender esses fundamentos é o
que MIT e Harvard ensinam antes de qualquer framework, e o que te faz raciocinar sobre eles em vez de
só apertar botões.

## 💡 Conceito (o porquê)

### Escala vertical vs horizontal
- **Vertical (scale up):** comprar uma máquina maior (mais CPU/RAM/disco). Simples, mas tem **teto
  físico** e fica exponencialmente caro — e continua sendo um **ponto único de falha**.
- **Horizontal (scale out):** adicionar **mais máquinas** (nós) e dividir o trabalho entre elas. Sem
  teto prático e mais barato por unidade — mas exige coordenar máquinas que falham de forma independente.

Sistemas de dados modernos escalam **horizontalmente**. É por isso que Kafka tem partições, Cassandra
tem nós e Spark tem workers: todos dividem para conquistar.

### Particionamento (sharding): dividir os dados
**Particionar** (ou *shard*) é quebrar um conjunto grande de dados em pedaços, cada um num nó
diferente, para que nenhuma máquina precise guardar (ou processar) tudo. A chave é **como dividir**:
- **Por intervalo (range):** faixas de valores (A–M num nó, N–Z noutro). Bom para varreduras por
  intervalo, mas arrisca **desbalanceamento** (uma faixa mais popular sobrecarrega um nó).
- **Por hash:** `hash(chave) % nº_de_nós` espalha uniformemente. Balanceia bem, mas perde a localidade
  de intervalo. É o que Kafka faz com a chave (M17) e Cassandra com a partition key (M18).

O objetivo é **balancear a carga** e evitar *hotspots* — um nó que recebe muito mais que os outros.

### Consistent hashing: adicionar/remover nós sem caos
Com `hash % N`, mudar o número de nós (N) **remapeia quase tudo** — um rebalanceamento caríssimo. O
**hashing consistente** resolve: nós e chaves são posicionados num "anel"; cada chave pertence ao
próximo nó no sentido horário. Ao adicionar/remover um nó, **só as chaves vizinhas** se movem, não
todas. É como sistemas distribuídos crescem elasticamente sem parar tudo.

### Replicação: cópias para sobreviver a falhas
Particionar espalha os dados, mas se o nó que guarda uma partição morre, aquela fatia **some**. Por
isso cada partição é **replicada** em vários nós (fator de replicação): se um cai, outro assume. Como
manter as réplicas em sincronia — e o que acontece quando elas divergem — é o tema da unidade 2.

### O problema fundamental: falhas parciais
Num único computador, ou funciona ou não funciona. Num sistema distribuído há um terceiro estado,
péssimo: **parte funciona e parte não**. Um nó pode estar **lento** (indistinguível de morto), a
**rede** pode perder ou atrasar mensagens, dois nós podem discordar de quem está vivo. Não há relógio
global confiável nem "verdade" instantânea compartilhada. **Falhas parciais são a regra, não a
exceção** — e projetar apesar delas (tolerância a falhas, timeouts, reprocessamento idempotente) é a
essência da engenharia distribuída.

## 🔎 Exemplo
Um tópico Kafka de eventos cresce além de um servidor. Você o **particiona** em 12 partições
espalhadas por 4 brokers (particionamento por hash da chave, M17), balanceando a carga. Cada partição
é **replicada** em 3 brokers (fator 3): se um broker cai — uma **falha parcial** —, as réplicas
assumem e nada se perde. Ao adicionar um 5º broker, o rebalanceamento move só uma fração das
partições. Escala horizontal + particionamento + replicação + tolerância a falhas: os quatro pilares,
juntos, num sistema que você já usou sem ver a engenharia por baixo.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann dedica capítulos a **particionamento**, **replicação** e ao capítulo "The Trouble with
Distributed Systems" (relógios não confiáveis, falhas parciais, rede assíncrona). Dean & Ghemawat, no
paper do **MapReduce**, mostram como dividir dados e computação por milhares de máquinas comuns,
tolerando falhas — o alicerce do Spark/Hadoop. — *Designing Data-Intensive Applications* (caps. 5, 6,
8); *MapReduce: Simplified Data Processing on Large Clusters*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
"Escala horizontal em hardware comum, tolerando falhas" é a ideia que o Google popularizou (GFS,
MapReduce) e que virou o padrão de toda a stack de dados moderna. A consequência prática: você projeta
assumindo que **máquinas vão falhar** o tempo todo — e o sistema continua. Ignorar isso é a causa de
incidentes em produção. — Dean & Ghemawat; Kleppmann.
:::

## ⚠️ Erros comuns
- **Escalar só verticalmente** até bater no teto físico (e no custo) — e manter um ponto único de falha.
- **Partition key ruim** — cria hotspots (um nó sobrecarregado) e desbalanceia o cluster.
- **`hash % N` para posicionar nós** — remapeia tudo ao mudar N; use hashing consistente.
- **Assumir rede confiável e relógio global** — a falácia clássica dos sistemas distribuídos.
- **Não replicar** — uma partição num só nó é um dado a um crash de distância de sumir.

## 💼 O que o mercado espera
Explicar por que se distribui (escala horizontal), como se particiona (range vs hash, hotspots,
consistent hashing) e por que replicação e tolerância a falhas parciais são inevitáveis. É a base
conceitual por trás de Kafka, Spark, Cassandra e do system design (M15).

:::{admonition} ✨ Em resumo
:class: resumo
- Distribui-se para **escalar horizontalmente** além do teto de uma máquina (e sem ponto único de falha).
- **Particionar (shard)** divide os dados por nós — por intervalo ou por **hash**; o alvo é balancear e evitar *hotspots*.
- **Consistent hashing** permite adicionar/remover nós movendo só as chaves vizinhas.
- **Replicação** dá tolerância a falhas; o problema central é a **falha parcial** (rede/relógio não confiáveis).
:::

## 🧠 Quiz de recall
1. Qual a diferença entre escala vertical e horizontal?
   :::{dropdown} Resposta
   Vertical = máquina maior (tem teto físico, custo alto, ponto único de falha); horizontal = mais máquinas dividindo o trabalho (sem teto prático, tolera falhas, mas exige coordenação).
   :::
2. O que é particionamento e quais as duas estratégias?
   :::{dropdown} Resposta
   Dividir os dados em pedaços por nó. Por intervalo (faixas de valores; bom para range, arrisca desbalanceamento) ou por hash (espalha uniforme, perde localidade). O alvo é balancear e evitar hotspots.
   :::
3. Que problema o consistent hashing resolve?
   :::{dropdown} Resposta
   Com hash % N, mudar N remapeia quase tudo. O hashing consistente move só as chaves vizinhas ao adicionar/remover um nó, permitindo crescer elasticamente.
   :::
4. Por que se replica além de particionar?
   :::{dropdown} Resposta
   Particionar espalha os dados, mas se o nó de uma partição cai, ela some. A replicação mantém cópias em outros nós para tolerar falhas.
   :::
5. O que é uma "falha parcial" e por que é o problema central?
   :::{dropdown} Resposta
   Parte do sistema funciona e parte não (nó lento indistinguível de morto, rede perdendo mensagens, sem relógio global). É a regra em distribuídos e força projetar com timeouts, tolerância a falhas e idempotência.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que não escalar verticalmente e evitar toda a complexidade distribuída?"
  :::{dropdown} Resposta modelo
  Porque a escala vertical tem teto físico, fica exponencialmente cara e mantém um ponto único de falha. Quando os dados ou a carga passam do que a maior máquina viável aguenta — ou preciso de alta disponibilidade —, distribuo horizontalmente: particiono os dados, replico para tolerar falhas e aceito a complexidade de coordenar máquinas que falham de forma independente. É o trade-off que Kafka/Spark/Cassandra já assumem.
  :::
- **P:** "Como você escolheria a chave de particionamento de um dataset enorme?"
  :::{dropdown} Resposta modelo
  Busco uma chave de alta cardinalidade que distribua a carga uniformemente e case com o padrão de acesso — normalmente por hash da chave para balancear. Evito chaves que criam hotspots (ex.: uma data corrente onde tudo cai na mesma partição). Se o cluster vai crescer, prefiro hashing consistente para não remapear tudo ao adicionar nós.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (caps. 6 particionamento, 8 falhas distribuídas).
- **Dean & Ghemawat — MapReduce** (dividir dados/computação tolerando falhas).
- **Reis & Housley — Fundamentals of Data Engineering** (sistemas distribuídos no ciclo de vida).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — particionamento e falhas. <!-- @kleppmann2017 -->
- Dean, J.; Ghemawat, S. *MapReduce: Simplified Data Processing on Large Clusters* (2004). <!-- @dean2004 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — sistemas distribuídos. <!-- @reis2022 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
