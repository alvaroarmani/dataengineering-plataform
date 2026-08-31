# Consenso e tolerância a falhas

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Vários nós precisam **concordar** sobre uma coisa: quem é o líder? Qual a ordem das operações? Este
evento já foi processado? Parece trivial — até você lembrar que os nós falham, a rede perde mensagens
e ninguém tem um relógio global (unidade 1). Fazer máquinas não confiáveis chegarem a um **acordo
confiável** é o **problema do consenso**, um dos mais profundos da computação distribuída — e ele está
por baixo de tudo que você usou: a eleição de líder de partição no Kafka, a coordenação do Cassandra,
o scheduler do Kubernetes (M20). Entender consenso e **tolerância a falhas** fecha a base distribuída.

## 💡 Conceito (o porquê)

### Por que consenso é difícil
Se um nó propõe "X é o novo líder" e não recebe resposta de outro, ele não sabe se: (a) o outro nó
morreu, (b) o outro está lento, ou (c) a **resposta** se perdeu na rede. Os três casos são
**indistinguíveis**. Sem relógio global e com mensagens que somem, garantir que todos concordem — e
não haja dois "líderes" agindo ao mesmo tempo (*split-brain*) — exige protocolos cuidadosos. Um
resultado teórico famoso (FLP) mostra que consenso perfeito é **impossível** numa rede totalmente
assíncrona com falhas; na prática, usa-se timeouts e maioria para contornar.

### Maioria (quórum) e o número mágico 2f + 1
A ferramenta central é a **maioria**: uma decisão só vale se **mais da metade** dos nós concordam.
Como dois subconjuntos que são "maioria" **sempre se intersectam**, não é possível dois grupos
decidirem coisas contraditórias. Consequência prática: para tolerar **f** falhas simultâneas, você
precisa de **N = 2f + 1** nós (a maioria, f+1, precisa sobreviver). Por isso clusters de coordenação
têm números **ímpares** — 3 nós toleram 1 falha, 5 toleram 2. Um número par não compra tolerância
extra e ainda arrisca empate.

### Algoritmos de consenso: Raft e Paxos
Protocolos como **Raft** e **Paxos** implementam consenso tolerante a falhas. O Raft (mais fácil de
entender) funciona por **eleição de líder** + **replicação de log**: os nós elegem um líder por maioria
de votos; o líder ordena as operações num log replicado; se ele cai, uma nova eleição escolhe outro —
sempre por maioria, o que impede split-brain. É assim que sistemas mantêm uma **ordem única e
consistente** de eventos mesmo com nós falhando.

### Onde consenso aparece na sua stack
- **Kafka:** elege o líder de cada partição e coordena o cluster (controller) via consenso.
- **Cassandra/Dynamo:** usam quóruns (R+W>N, unidade 2) e, para operações que exigem, protocolos de acordo.
- **ZooKeeper / etcd:** serviços de coordenação dedicados (consenso como serviço) usados por muitos
  sistemas — inclusive o **etcd** que guarda o estado do **Kubernetes** (M20).
- **Bancos NewSQL** (Spanner, CockroachDB): consenso (Paxos/Raft) para transações distribuídas consistentes.

### Tolerância a falhas na prática
Consenso é caro (exige rodadas de mensagens e maioria viva), então se reserva para o que **precisa**
de acordo forte (quem é líder, ordem do log). O resto usa técnicas mais baratas já vistas: replicação,
**retries com timeout**, **idempotência** (M08/M09/M17 — reprocessar sem duplicar) e *health checks*.
A arte é escolher a garantia mais fraca (e barata) que ainda atende o requisito.

## 🔎 Exemplo
Um cluster Kafka de 3 brokers precisa de um **controller** (o nó que coordena partições e elege
líderes). Os brokers usam consenso por **maioria**: com 3 nós, toleram **1 falha** (2f+1 com f=1). Se
o controller cai, os 2 restantes formam maioria e elegem um novo — sem risco de dois controllers agindo
(split-brain), porque dois grupos majoritários não coexistem. O estado de metadados é replicado como um
**log ordenado** por consenso. É por isso que você monta clusters de coordenação com **3 ou 5** nós,
nunca 2 ou 4.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann cobre **consenso**, eleição de líder, o perigo do split-brain e por que a **maioria** é a
base da tolerância a falhas, situando Paxos/Raft e serviços como o ZooKeeper. — *Designing
Data-Intensive Applications* (cap. 9, "Consistency and Consensus").
:::

:::{admonition} 🏭 Do mundo real
:class: important
Quase todo sistema distribuído "sério" delega a parte mais difícil (consenso) a um componente
especializado — ZooKeeper, etcd, ou um protocolo Raft embutido — em vez de reinventá-lo. É por isso que
o etcd é o coração do Kubernetes e que você vê clusters de coordenação sempre com número **ímpar** de
nós. Reimplementar consenso à mão é uma das formas mais rápidas de criar bugs sutis de dados. — Kleppmann.
:::

## ⚠️ Erros comuns
- **Número par de nós** num cluster de consenso — não aumenta a tolerância e arrisca empate.
- **Ignorar split-brain** — dois "líderes" simultâneos corrompem dados; a maioria é o que previne.
- **Reimplementar consenso à mão** — em vez de usar Raft/etcd/ZooKeeper prontos.
- **Usar consenso para tudo** — é caro; reserve para o que exige acordo forte, use idempotência no resto.
- **Confundir nó lento com nó morto** — a base de muitas decisões erradas de failover.

## 💼 O que o mercado espera
Entender por que consenso é difícil, a regra 2f+1/maioria, o papel de Raft/Paxos e de ZooKeeper/etcd, e
como isso sustenta Kafka, Cassandra e Kubernetes. Não se espera implementar Raft, mas **raciocinar**
sobre tolerância a falhas e quórum.

:::{admonition} ✨ Em resumo
:class: resumo
- **Consenso** = fazer nós não confiáveis concordarem; difícil porque nó lento ≡ nó morto e mensagens somem.
- A **maioria** previne decisões contraditórias e split-brain; tolerar **f** falhas exige **N = 2f + 1** (nº ímpar).
- **Raft/Paxos** implementam consenso via eleição de líder + log replicado; **ZooKeeper/etcd** oferecem isso como serviço.
- Consenso é caro — reserve-o para acordo forte (líder, ordem) e use replicação + **idempotência** no resto.
:::

## 🧠 Quiz de recall
1. Por que consenso é difícil num sistema distribuído?
   :::{dropdown} Resposta
   Porque um nó não distingue se o outro morreu, está lento ou se a resposta se perdeu; sem relógio global e com mensagens que somem, é difícil garantir acordo sem dois líderes (split-brain).
   :::
2. Por que N = 2f + 1?
   :::{dropdown} Resposta
   Para tolerar f falhas, a maioria (f+1) precisa sobreviver; logo são necessários 2f+1 nós. Duas maiorias sempre se intersectam, evitando decisões contraditórias.
   :::
3. Por que clusters de coordenação usam número ímpar de nós?
   :::{dropdown} Resposta
   Porque um nó par a mais não aumenta a tolerância (3 e 4 toleram 1) e ainda arrisca empate; ímpares maximizam a tolerância pelo custo.
   :::
4. O que Raft faz, em alto nível?
   :::{dropdown} Resposta
   Elege um líder por maioria de votos e replica um log ordenado de operações; se o líder cai, nova eleição por maioria escolhe outro, impedindo split-brain.
   :::
5. Onde consenso aparece na stack de dados?
   :::{dropdown} Resposta
   Eleição de líder de partição no Kafka, coordenação via ZooKeeper/etcd, estado do Kubernetes (etcd), transações de bancos NewSQL (Spanner/CockroachDB).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Quantos nós num cluster de coordenação e por quê?"
  :::{dropdown} Resposta modelo
  Um número ímpar — tipicamente 3 ou 5. Com 2f+1 nós tolero f falhas mantendo maioria viva: 3 toleram 1, 5 toleram 2. Números pares não compram tolerância extra (4 tolera as mesmas 1 falha que 3) e ainda arriscam empate na eleição. A maioria é o que evita split-brain.
  :::
- **P:** "Você precisa garantir ordem única de eventos com nós que falham. Como aborda?"
  :::{dropdown} Resposta modelo
  Não reimplemento consenso: uso um sistema que já resolve isso — um log ordenado com eleição de líder por maioria (estilo Raft), como o Kafka faz por partição, ou delego a coordenação a etcd/ZooKeeper. Para o processamento derivado, torno as operações idempotentes para tolerar reprocessamento. Reservo o consenso caro só para o que exige acordo forte.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 9, consenso e consistência).
- **Documentação do Raft** (raft.github.io) — consenso compreensível.
- **Documentação do etcd / ZooKeeper** — consenso como serviço (base do Kubernetes).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — consenso e tolerância a falhas. <!-- @kleppmann2017 -->
- Dean, J.; Ghemawat, S. *MapReduce* (2004) — tolerância a falhas em larga escala. <!-- @dean2004 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — coordenação distribuída. <!-- @reis2022 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
