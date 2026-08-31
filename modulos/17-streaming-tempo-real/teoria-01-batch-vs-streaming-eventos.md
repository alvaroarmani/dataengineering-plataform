# Batch vs streaming e o modelo de eventos

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Até aqui, seus pipelines rodaram em **lotes**: uma vez por hora ou por dia, o Airflow (M09)
processa "tudo o que chegou desde a última vez". Isso é ótimo para relatórios diários — mas
péssimo quando o negócio precisa **reagir agora**: detectar uma fraude no cartão em segundos,
atualizar o estoque enquanto o cliente compra, alimentar um painel ao vivo. Nesses casos, esperar
o próximo lote é tarde demais. **Streaming** é o processamento de dados **em movimento**, evento a
evento, à medida que acontecem — e entender quando ele é necessário (e quando é exagero) é uma
decisão de arquitetura que separa o júnior do pleno.

## 💡 Conceito (o porquê)

### Batch vs streaming
- **Batch (lote):** processa um **conjunto finito** de dados acumulados, em intervalos. Simples,
  barato, fácil de reprocessar. Latência = o tamanho da janela (minutos a horas).
- **Streaming (fluxo):** processa um **fluxo ilimitado** de eventos, continuamente, com latência de
  **segundos ou menos**. Mais poderoso para reação imediata — e mais complexo (estado, ordem,
  falhas em processo contínuo).

A regra de ouro (M15, system design): **a latência exigida decide**. Se "de hora em hora" atende,
batch vence pela simplicidade. Se o negócio precisa reagir em segundos, é streaming. Escolher
streaming sem necessidade é *over-engineering*.

### O que é um "evento"
Um **evento** é um fato imutável que aconteceu num instante: "cliente 42 comprou o produto 7 às
10:03", "sensor X leu 91°C". Ele não é um comando ("faça algo") — é um **registro do que ocorreu**.
Streaming trata os dados como um **fluxo de eventos** em vez de tabelas que você consulta.

### Arquitetura orientada a eventos (event-driven)
Em vez de um serviço **perguntar** ao outro ("tem pedido novo?"), quem gera o evento o **publica**,
e quem se interessa **reage**. Isso desacopla produtores de consumidores: o produtor não sabe (nem
precisa saber) quem consome. Um mesmo evento ("pedido criado") pode alimentar, ao mesmo tempo, o
faturamento, o estoque e o antifraude — cada um no seu ritmo. Esse desacoplamento é o que torna
sistemas de dados **escaláveis e evolutivos**.

### Onde streaming se encaixa no pipeline
Streaming não substitui o warehouse: **alimenta** as camadas. Um padrão comum: eventos entram por
um broker (Kafka), são processados em tempo real para reações imediatas **e** aterrissam no data
lake/warehouse (M06/M11) para análise histórica. Daí surgem as arquiteturas **Lambda** (uma trilha
batch + uma trilha streaming) e **Kappa** (tudo como stream, o batch é só um caso do stream).

### CDC: transformar mudanças de banco em eventos
**Change Data Capture** lê o log de transações de um banco (OLTP) e emite cada INSERT/UPDATE/DELETE
como um **evento** de stream. É a ponte mais comum entre os sistemas transacionais e a plataforma de
dados: em vez de "puxar a tabela toda toda noite", você recebe as mudanças em tempo real.

## 🔎 Exemplo
Uma fintech precisa barrar transações fraudulentas **antes** de aprová-las. Batch diário não serve —
a fraude já aconteceu. A solução: cada transação vira um **evento** publicado num broker; um serviço
de antifraude **consome** o fluxo, avalia em milissegundos e aprova/bloqueia; o mesmo evento também
cai no data lake para treinar o modelo e para relatórios. Um evento, vários consumidores, latência
de segundos — impossível com batch.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann dedica um capítulo aos **fluxos de eventos**, tratando o streaming como a generalização do
batch para dados ilimitados e destacando o **log** como abstração central. Reis & Housley posicionam
batch e streaming como escolhas do ciclo de vida guiadas por latência e caso de uso. — *Designing
Data-Intensive Applications* (cap. 11); *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Empresas como Nubank, iFood e Netflix usam plataformas de eventos (Kafka e afins) como **espinha
dorsal**: pedidos, cliques e transações viram streams que alimentam simultaneamente reação em tempo
real e analytics. O padrão "publique o evento uma vez, muitos consomem" é o que sustenta essa escala.
— prática de mercado; Kleppmann.
:::

## ⚠️ Erros comuns
- **Streaming por moda** — usar onde batch bastava; paga-se em complexidade sem ganho.
- **Confundir evento com comando** — evento é fato ocorrido, não ordem para agir.
- **Acoplar produtor e consumidor** — perde-se o desacoplamento que justifica eventos.
- **Achar que streaming substitui o DW** — ele alimenta as camadas; a análise histórica continua.
- **Ignorar o custo operacional** — stream roda 24/7; exige monitoramento contínuo (M12).

## 💼 O que o mercado espera
Saber definir evento e arquitetura orientada a eventos, decidir batch vs streaming por requisito de
latência, e entender CDC e os padrões Lambda/Kappa. "Quando você usaria streaming em vez de batch?"
é pergunta recorrente.

:::{admonition} ✨ Em resumo
:class: resumo
- **Batch** processa lotes finitos em intervalos; **streaming** processa um fluxo ilimitado de eventos em tempo quase real.
- A **latência exigida decide** — streaming sem necessidade é over-engineering.
- **Evento** = fato imutável ocorrido; **event-driven** desacopla quem publica de quem reage.
- Streaming **alimenta** o lake/warehouse (Lambda/Kappa); **CDC** transforma mudanças de banco em eventos.
:::

## 🧠 Quiz de recall
1. Qual a diferença essencial entre batch e streaming?
   :::{dropdown} Resposta
   Batch processa um conjunto finito acumulado em intervalos (latência = janela); streaming processa um fluxo ilimitado de eventos continuamente, com latência de segundos ou menos.
   :::
2. O que decide entre batch e streaming?
   :::{dropdown} Resposta
   A latência exigida pelo negócio: se janelas (ex.: horária) atendem, batch (mais simples/barato); se precisa reagir em segundos, streaming.
   :::
3. O que é um "evento" e como difere de um comando?
   :::{dropdown} Resposta
   Um evento é um fato imutável que ocorreu num instante (registro do que aconteceu); um comando é uma ordem para fazer algo. Streaming trata dados como fluxo de eventos.
   :::
4. O que a arquitetura orientada a eventos desacopla, e por quê isso importa?
   :::{dropdown} Resposta
   Desacopla o produtor do consumidor: quem gera publica, quem se interessa reage. Permite que muitos consumidores usem o mesmo evento independentemente, dando escala e evolução.
   :::
5. O que é CDC e para que serve?
   :::{dropdown} Resposta
   Change Data Capture lê o log de transações de um banco e emite cada mudança (INSERT/UPDATE/DELETE) como evento — a ponte em tempo real entre o OLTP e a plataforma de dados.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Quando você escolheria streaming em vez de batch?"
  :::{dropdown} Resposta modelo
  Parto do requisito de latência e do caso de uso. Se o negócio precisa reagir em segundos — antifraude, estoque ao vivo, alertas — streaming se justifica. Se relatórios de hora/dia atendem, fico no batch, que é mais simples, barato e fácil de reprocessar. Também considero o custo operacional: stream roda 24/7 e exige monitoramento. Ou seja, streaming por necessidade, não por moda.
  :::
- **P:** "Como um mesmo evento de 'pedido criado' serve a vários times?"
  :::{dropdown} Resposta modelo
  Publico o evento uma vez num broker (Kafka) e cada time o consome de forma independente: faturamento, estoque e antifraude leem o mesmo tópico no seu próprio ritmo, sem acoplamento. O produtor não precisa saber quem consome. Isso é o cerne do event-driven e o que dá escala — e o evento ainda pode aterrissar no lake para analytics.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 11, fluxos de eventos e logs).
- **Reis & Housley — Fundamentals of Data Engineering** (batch vs streaming no ciclo de vida).
- **Densmore — Data Pipelines Pocket Reference** (padrões de ingestão e streaming).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 11, streams. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — batch vs streaming. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — padrões de ingestão/streaming. <!-- @densmore2021 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
