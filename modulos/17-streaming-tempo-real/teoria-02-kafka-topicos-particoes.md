# Kafka: tópicos, partições, offsets e consumer groups

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você decidiu que precisa de streaming (unidade 1). Como, na prática, milhares de eventos por segundo
saem de centenas de produtores e chegam, **em ordem, sem perder e sem duplicar**, a dezenas de
consumidores independentes — cada um no seu ritmo, alguns lendo o histórico, outros só o novo? Essa
é a engenharia difícil do tempo real, e a resposta que virou padrão de mercado é o **Apache Kafka**:
um **log distribuído** durável. Entender seu modelo — tópicos, partições, offsets, consumer groups —
é o que permite raciocinar sobre desempenho, ordem e garantias em qualquer sistema de streaming.

## 💡 Conceito (o porquê)

### Kafka é um log, não uma fila
Numa fila tradicional, ler uma mensagem a **remove**. No Kafka, os eventos são anexados a um **log**
append-only e **permanecem** por um período de retenção configurável. Cada consumidor lê no seu
próprio ponto, e vários consumidores independentes leem os **mesmos** eventos. Isso é o que viabiliza
"publique uma vez, muitos consomem" (unidade 1): o log é a fonte da verdade, releitura é natural.

### Tópicos e partições
- Um **tópico** é um fluxo nomeado de eventos (ex.: `pedidos`).
- Cada tópico é dividido em **partições** — logs independentes que podem viver em máquinas
  diferentes. A partição é a **unidade de paralelismo e de ordem**.
- Cada evento numa partição recebe um **offset**: um número sequencial crescente (0, 1, 2, …) que o
  identifica e ordena **dentro daquela partição**.

**Consequência central:** a ordem é garantida **por partição**, não no tópico inteiro. Se você
precisa que todos os eventos de um mesmo cliente sejam processados em ordem, todos eles precisam cair
na **mesma partição**.

### Chave da mensagem e particionamento
Ao publicar, o produtor pode dar uma **chave** ao evento (ex.: `cliente_id`). O Kafka decide a
partição por `hash(chave) % nº_de_partições` — então **a mesma chave sempre vai para a mesma
partição** (enquanto o número de partições não muda). Assim você garante ordem por cliente sem
sacrificar o paralelismo entre clientes diferentes. Sem chave, os eventos se espalham (balanceados),
maximizando throughput mas sem garantia de ordem entre eles.

### Produtores e consumidores
- **Produtor (producer):** publica eventos num tópico (opcionalmente com chave).
- **Consumidor (consumer):** lê eventos de um tópico, avançando seu **offset**. Ele controla o
  ritmo e pode reprocessar voltando o offset (releitura do histórico).

### Consumer groups: paralelismo e balanceamento
Consumidores que compartilham o mesmo **group id** formam um **consumer group** e **dividem** as
partições entre si — cada partição é lida por **exatamente um** membro do grupo. Isso escala o
consumo horizontalmente:
- Nº de consumidores ativos ≤ nº de partições (partições a mais ficam ociosas).
- Grupos **diferentes** recebem **todos** os eventos, independentemente (é assim que faturamento e
  antifraude leem o mesmo `pedidos` sem interferir um no outro).

### Offset commitado e durabilidade
O grupo **commita** o offset até onde já processou; se um consumidor cair, outro assume a partição a
partir do último offset commitado. Combinado com **replicação** das partições entre brokers, o Kafka
sobrevive à queda de máquinas sem perder eventos — a durabilidade que uma fila em memória não dá.

## 🔎 Exemplo
O tópico `pedidos` tem 3 partições. Os produtores publicam com chave `cliente_id`. Todos os eventos
do cliente 42 caem sempre na partição `hash(42) % 3` — então são lidos **em ordem**. O time de
faturamento roda um consumer group `faturamento` com 3 consumidores (um por partição = paralelismo
máximo); o time de antifraude roda outro group `antifraude`, que recebe **os mesmos** eventos de
forma independente. Se um consumidor do faturamento cai, o grupo redistribui sua partição para outro
membro, que continua do último offset commitado. Nada se perde, nada duplica desnecessariamente.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann apresenta o **log particionado** (o modelo do Kafka) como a ponte entre mensageria e bancos
de dados: durável, releível e ordenado por partição, com offsets como cursores dos consumidores. — 
*Designing Data-Intensive Applications* (cap. 11, "Partitioned Logs").
:::

:::{admonition} 🏭 Do mundo real
:class: important
Dimensionar o **número de partições** é uma decisão de projeto real: ele fixa o teto de paralelismo
de consumo (nunca mais consumidores úteis que partições) e afeta a ordem. Aumentar partições depois
**muda o mapeamento chave→partição**, o que pode bagunçar a ordem de chaves existentes — por isso se
planeja a partição-chave com folga desde o início. — prática de mercado; Kleppmann.
:::

## ⚠️ Erros comuns
- **Esperar ordem global** num tópico com várias partições — a ordem é **por partição**.
- **Não usar chave** quando a ordem por entidade importa — eventos do mesmo cliente se espalham.
- **Mais consumidores que partições** no grupo — os excedentes ficam ociosos.
- **Confundir fila com log** — no Kafka ler não apaga; a retenção e a releitura são recursos.
- **Ignorar o commit de offset** — sem commit correto, quedas causam reprocessamento ou perda.

## 💼 O que o mercado espera
Explicar tópico/partição/offset/consumer group, saber que a ordem é por partição e como a chave
controla o particionamento, e entender por que grupos diferentes recebem todos os eventos. É o
alicerce de qualquer conversa sobre Kafka em entrevista.

:::{admonition} ✨ Em resumo
:class: resumo
- Kafka é um **log distribuído durável**: ler não apaga; muitos consumidores releem os mesmos eventos.
- **Tópico → partições**; a partição é a unidade de **paralelismo e de ordem**; o **offset** ordena dentro dela.
- A **chave** define a partição (`hash(chave)`), garantindo ordem por entidade sem perder paralelismo.
- **Consumer group** divide as partições entre membros (1 partição → 1 membro); **grupos diferentes** recebem tudo.
:::

## 🧠 Quiz de recall
1. Por que Kafka é um "log" e não uma "fila"?
   :::{dropdown} Resposta
   Porque os eventos são anexados a um log append-only e permanecem por um período de retenção; ler não os remove, então vários consumidores releem os mesmos eventos no seu próprio offset.
   :::
2. Em que nível o Kafka garante ordem?
   :::{dropdown} Resposta
   Por partição — os offsets ordenam os eventos dentro de uma partição; não há ordem global entre partições de um tópico.
   :::
3. Como a chave da mensagem afeta o particionamento?
   :::{dropdown} Resposta
   O Kafka escolhe a partição por hash da chave, então a mesma chave vai sempre para a mesma partição — garantindo ordem por entidade (ex.: por cliente) sem perder paralelismo entre chaves diferentes.
   :::
4. O que é um consumer group e como ele escala o consumo?
   :::{dropdown} Resposta
   Consumidores com o mesmo group id que dividem as partições — cada partição é lida por exatamente um membro. Mais membros = mais paralelismo, até o limite do nº de partições.
   :::
5. Por que faturamento e antifraude não interferem um no outro lendo o mesmo tópico?
   :::{dropdown} Resposta
   Porque são consumer groups diferentes; cada grupo recebe todos os eventos de forma independente, com seus próprios offsets.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Preciso processar em ordem todos os eventos de cada usuário. Como configuro o Kafka?"
  :::{dropdown} Resposta modelo
  Uso o `user_id` como **chave** da mensagem: o Kafka manda todos os eventos de um usuário para a mesma partição, e a ordem é garantida por partição. Dimensiono o número de partições pensando no paralelismo desejado (o teto de consumidores úteis do grupo) e evito aumentar partições depois, o que mudaria o mapeamento chave→partição e bagunçaria a ordem de chaves existentes.
  :::
- **P:** "Meu consumer group tem 5 consumidores mas o tópico tem 3 partições. O que acontece?"
  :::{dropdown} Resposta modelo
  Só 3 consumidores ficam ativos (um por partição); os outros 2 ficam ociosos, prontos para assumir se algum cair (failover). Para aproveitar os 5, eu precisaria de pelo menos 5 partições. É por isso que o número de partições define o teto de paralelismo de consumo.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 11, "Partitioned Logs").
- **Documentação do Apache Kafka** — conceitos de tópicos, partições e consumer groups.
- **Reis & Housley — Fundamentals of Data Engineering** (ingestão em streaming).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 11, logs particionados. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — ingestão em streaming. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — brokers e streaming. <!-- @densmore2021 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
