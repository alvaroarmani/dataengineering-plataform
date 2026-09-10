# Microserviços e integração orientada a eventos

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Um sistema real não é um bloco só: é o app de pedidos, o serviço de pagamento, o estoque, o
antifraude, o data pipeline — cada um evoluindo separado, muitas vezes por times diferentes. Como
eles conversam **sem virar um novelo** onde mexer num quebra todos? Se cada serviço **chama
diretamente** os outros (síncrono), um serviço lento ou fora do ar derruba a cadeia inteira, e
adicionar um novo consumidor exige mexer no produtor. A resposta que a indústria consolidou —
**microserviços integrados por eventos** — é a mesma ideia do streaming (M17), agora como estilo de
**arquitetura de integração**. Entender isso conecta seus pipelines ao resto do sistema.

## 💡 Conceito (o porquê)

### Microserviços: dividir para evoluir
Em vez de um **monólito** (tudo num sistema só), a aplicação é dividida em **microserviços** —
serviços pequenos, independentes, cada um dono de um domínio (pagamento, estoque) e do seu próprio
dado, comunicando-se por rede. Ganha-se evolução e escala independentes; paga-se em complexidade de
integração (agora há uma **rede** não confiável entre eles — M19). Para o engenheiro de dados, cada
microserviço é uma **fonte de dados** (e às vezes um consumidor do seu pipeline).

### Comunicação síncrona vs assíncrona
Há duas formas de os serviços conversarem:
- **Síncrona (request/response):** o serviço A **chama** o B e **espera** a resposta (REST/RPC,
  unidade 1). Simples e imediato — mas **acopla**: se B está lento/fora, A trava. E A precisa
  **saber** quem chamar.
- **Assíncrona (via eventos/mensagens):** A **publica** um evento num broker e segue a vida; quem se
  interessa **consome** quando puder. **Desacopla** produtor de consumidor (nenhum precisa conhecer o
  outro) e absorve picos (a fila segura a carga). É a arquitetura **event-driven** (M17).

A escolha é de projeto: síncrono quando você precisa da resposta **agora** (ex.: validar cartão);
assíncrono quando pode processar **depois** e quer resiliência/desacoplamento (ex.: atualizar
analytics, enviar email).

### Filas de mensagens: RabbitMQ vs Kafka
O intermediário assíncrono é um **message broker**. Dois estilos:
- **Fila de tarefas (ex.: RabbitMQ):** distribui **tarefas** entre workers; tipicamente a mensagem é
  **consumida e some** (uma tarefa, um worker a executa). Ótimo para "processar este trabalho".
- **Log de eventos (ex.: Kafka, M17):** o evento **fica** (retenção); **vários** consumidores
  independentes releem o mesmo fluxo. Ótimo para "este fato aconteceu, quem quiser reage".

Regra prática: **fila de trabalho → RabbitMQ**; **stream de eventos com muitos consumidores → Kafka**.

### O padrão produtor/consumidor
Em ambos, o modelo é **produtor** (gera mensagens) e **consumidor** (processa). O consumidor
**confirma** (ack) o que processou; se cair antes do ack, a mensagem é reentregue (garantia de
entrega — daí a idempotência, unidade 3). Escala-se somando consumidores (como os consumer groups do
M17).

### Event-driven e o pipeline de dados
Isto liga diretamente ao seu trabalho: um evento "pedido criado" publicado uma vez alimenta, **em
paralelo e desacoplado**, o faturamento, o estoque **e** o seu pipeline analítico (que o joga no
lake/warehouse). Adicionar um novo consumidor (um novo dashboard, um modelo) **não mexe** no
produtor. É assim que a plataforma de dados se pluga no sistema sem acoplar tudo.

## 🔎 Exemplo
No checkout, o serviço de pedidos precisa **validar o pagamento agora** — então chama o serviço de
pagamento de forma **síncrona** (REST) e espera o "aprovado". Feito isso, publica um evento **"pedido
criado"** num broker (assíncrono) e segue. Três consumidores independentes reagem no seu ritmo: o
**estoque** dá baixa, o serviço de **email** confirma a compra, e o **pipeline de dados** ingere o
evento para o warehouse. Se o serviço de email cair, os outros seguem e a mensagem dele é reprocessada
depois. Síncrono onde a resposta é necessária; assíncrono/event-driven para desacoplar o resto.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann contrasta comunicação **síncrona (REST/RPC)** com **mensageria assíncrona** (brokers, filas
e logs de eventos), destacando o desacoplamento e a tolerância a falhas do modelo baseado em
mensagens. Reis & Housley tratam eventos e mensageria como fonte e coluna vertebral de ingestão. —
*Designing Data-Intensive Applications* (cap. 4 e 11); *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Empresas modernas usam eventos como "sistema nervoso": um fato publicado uma vez alimenta operação e
analytics em paralelo. O erro comum é fazer **tudo síncrono** — aí um serviço lento derruba a cadeia e
cada novo consumidor exige mexer no produtor. Reservar o síncrono para "preciso da resposta agora" e
usar eventos para o resto é o padrão maduro. — Kleppmann; prática de mercado.
:::

## ⚠️ Erros comuns
- **Tudo síncrono** — acoplamento e efeito dominó (um serviço lento trava a cadeia).
- **Produtor conhecendo os consumidores** — perde-se o desacoplamento; use eventos.
- **Escolher o broker errado** — fila de tarefas (RabbitMQ) vs log de eventos (Kafka) resolvem coisas diferentes.
- **Esquecer o ack/entrega** — sem confirmar o processamento, há perda ou reentrega mal tratada.
- **Assíncrono onde precisa de resposta imediata** — validar pagamento por evento é pedir problema.

## 💼 O que o mercado espera
Explicar microserviços vs monólito, síncrono (REST/RPC) vs assíncrono (mensageria), a diferença
RabbitMQ (fila de tarefas) × Kafka (log de eventos), e como o pipeline de dados se pluga via eventos.
Aparece em system design de integração.

:::{admonition} ✨ Em resumo
:class: resumo
- **Microserviços**: serviços independentes por domínio; cada um é uma fonte/consumidor de dados.
- **Síncrono (REST/RPC)** acopla e espera — use quando precisa da resposta **agora**; **assíncrono (eventos)** desacopla e resiste a picos.
- **RabbitMQ** = fila de tarefas (mensagem consumida some); **Kafka** = log de eventos (fica, muitos consumidores).
- **Event-driven** liga o pipeline ao sistema: um evento alimenta operação e analytics **sem acoplar**.
:::

## 🧠 Quiz de recall
1. O que são microserviços e o que muda para o engenheiro de dados?
   :::{dropdown} Resposta
   Serviços pequenos e independentes por domínio, cada um dono do seu dado, comunicando por rede. Para dados, cada microserviço é uma fonte (e às vezes consumidor do pipeline).
   :::
2. Síncrono vs assíncrono — quando usar cada um?
   :::{dropdown} Resposta
   Síncrono (REST/RPC) quando precisa da resposta agora (ex.: validar pagamento) — mas acopla. Assíncrono (eventos) quando pode processar depois e quer desacoplamento/resiliência.
   :::
3. Diferença entre RabbitMQ e Kafka?
   :::{dropdown} Resposta
   RabbitMQ é fila de tarefas (a mensagem é consumida e some; distribui trabalho). Kafka é log de eventos (o evento fica; vários consumidores releem o mesmo fluxo).
   :::
4. Por que event-driven desacopla?
   :::{dropdown} Resposta
   O produtor publica o evento sem saber quem consome; consumidores reagem no seu ritmo e novos consumidores entram sem mexer no produtor.
   :::
5. O que é o ack e por que importa?
   :::{dropdown} Resposta
   A confirmação de que o consumidor processou a mensagem; sem ela (queda antes do ack), a mensagem é reentregue — o que exige idempotência.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Quando você usaria comunicação síncrona e quando eventos entre serviços?"
  :::{dropdown} Resposta modelo
  Síncrono (REST/RPC) quando preciso da resposta imediata para prosseguir — validar um pagamento no checkout. Eventos (assíncrono) para tudo que pode ser processado depois e onde quero desacoplar: notificar estoque, enviar email, alimentar o pipeline analítico. Assim um consumidor lento não derruba a cadeia e adiciono novos consumidores sem tocar no produtor. Uso o broker certo: RabbitMQ para filas de tarefa, Kafka para stream de eventos com muitos consumidores.
  :::
- **P:** "Como o pipeline de dados se integra a uma arquitetura de microserviços?"
  :::{dropdown} Resposta modelo
  Como mais um consumidor de eventos. Os serviços publicam fatos ("pedido criado") num broker; meu pipeline consome esse fluxo (idempotente) e o materializa no lake/warehouse, em paralelo com os consumidores operacionais. Isso me dá dados em (quase) tempo real sem acoplar ao produtor, e novos eventos/consumidores entram sem quebrar o que existe. Também posso ingerir por API/CDC quando o serviço não publica eventos.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 4 e 11, RPC/mensageria/eventos).
- **Reis & Housley — Fundamentals of Data Engineering** (mensageria e eventos na ingestão).
- **Documentação de RabbitMQ e Apache Kafka** (filas × log de eventos).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — mensageria e eventos. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — eventos na ingestão. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — brokers e integração. <!-- @densmore2021 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
