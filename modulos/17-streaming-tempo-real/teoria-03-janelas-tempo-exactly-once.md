# Tempo de evento, janelas e semântica de entrega

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Num stream **ilimitado**, uma pergunta simples fica difícil: "quantos pedidos por minuto?". Em batch
você tem um conjunto fechado e conta. No stream os eventos **nunca acabam** — e pior, chegam **fora
de ordem** e **atrasados** (um celular sem rede envia o evento 30s depois de o clique acontecer). Além
disso, sistemas contínuos falham no meio: como garantir que uma falha não **perca** nem **duplique** o
resultado? Esta unidade fecha o streaming com os três conceitos que tornam o tempo real confiável:
**tempo de evento**, **janelas** e **semântica de entrega**.

## 💡 Conceito (o porquê)

### Tempo de evento vs tempo de processamento
- **Tempo de evento (event time):** quando o fato **aconteceu** (o clique foi às 10:03:00).
- **Tempo de processamento (processing time):** quando o sistema **viu** o evento (chegou às 10:03:28).

Para métricas corretas, o que importa quase sempre é o **tempo de evento** — senão um atraso de rede
joga o clique das 10:03 no minuto errado. Processar por tempo de processamento é mais simples, mas
distorce qualquer agregação temporal.

### Janelas (windows)
Como um stream é infinito, agregações precisam de **janelas** — recortes finitos de tempo:
- **Tumbling (fixa):** blocos que não se sobrepõem (ex.: cada minuto cheio). "Pedidos por minuto."
- **Sliding (deslizante):** janelas que se sobrepõem (ex.: últimos 5 min, atualizando a cada 1 min).
- **Session (sessão):** agrupa eventos próximos no tempo, separados por períodos de inatividade
  (ex.: uma "sessão" de navegação do usuário).

A janela transforma "contar o infinito" em "contar cada intervalo" — a ponte entre stream e agregação.

### Watermarks: até quando esperar os atrasados
Se eventos chegam atrasados, quando você **fecha** a janela do minuto 10:03? Cedo demais e você perde
os atrasados; tarde demais e a métrica nunca sai. Um **watermark** é a decisão explícita de "já vi
eventos suficientes até o tempo T; considero as janelas até T completas" — o equilíbrio entre
**completude** e **latência**. Eventos que chegam depois do watermark são tratados à parte (descartados
ou reconciliados).

### Semântica de entrega
Em processamento contínuo com falhas, há três garantias possíveis:
- **At-most-once (no máximo uma vez):** pode **perder** eventos, nunca duplica. Raro (só onde perda é aceitável).
- **At-least-once (ao menos uma vez):** nunca perde, mas pode **duplicar** (reprocessa após falha). O padrão comum.
- **Exactly-once (exatamente uma vez):** nem perde nem duplica no resultado. O ideal — e o mais caro.

Na prática, **at-least-once + idempotência** entrega o efeito de exactly-once: se o processamento é
idempotente (reprocessar não muda o resultado — via chave/dedup, como no M08/M09), duplicatas de
entrega não corrompem o estado. É a estratégia mais usada.

### Estado (stateful processing)
Agregar por janela exige **guardar estado** (a contagem parcial de cada janela) enquanto os eventos
chegam. Frameworks de stream gerenciam esse estado com tolerância a falhas (checkpoints), para que uma
queda não perca as contagens em andamento. Isso é o que diferencia um processador de stream de um
simples "for each evento".

### Panorama: Kafka Streams e Flink
- **Kafka Streams:** biblioteca (roda no seu app) para transformar/agregar tópicos Kafka com estado e
  janelas — ótimo quando você já vive no Kafka.
- **Apache Flink:** engine de streaming dedicada, forte em tempo de evento, watermarks e exactly-once —
  referência para processamento de stream sofisticado.
- **Spark Structured Streaming** (M11) traz streaming ao mundo Spark, em micro-batches.

## 🔎 Exemplo
Painel de "pedidos por minuto" de um app de delivery. Cada pedido carrega seu **event time**. Uma
janela **tumbling de 1 minuto** agrupa por tempo de evento — então o pedido feito às 10:03:59 que
chegou às 10:04:02 (atrasado) ainda entra no minuto 10:03, correto. Um **watermark** de 10s decide
fechar a janela 10:03 só às 10:04:10, tolerando pequenos atrasos. O processamento é **at-least-once +
idempotente** (a contagem por minuto é sobrescrita, não somada), então um reprocessamento após falha
não infla os números. Resultado: métrica temporal correta, resiliente e em tempo quase real.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann trata tempo de evento vs processamento, janelas e o problema dos eventos atrasados, e discute
as garantias **exactly-once** como combinação de reprocessamento com operações idempotentes/transacionais.
— *Designing Data-Intensive Applications* (cap. 11).
:::

:::{admonition} 🏭 Do mundo real
:class: important
"Exactly-once" quase nunca é mágica do broker: na prática é **at-least-once + idempotência** no
consumidor (chaves, upserts, dedup — o que você já praticou no batch, M08/M09). Projetar o
processamento para ser idempotente é o que torna o streaming confiável sob falhas. — prática de
mercado; Kleppmann.
:::

## ⚠️ Erros comuns
- **Agregar por tempo de processamento** — atrasos de rede jogam eventos no intervalo errado.
- **Fechar janelas sem watermark** — ou perde atrasados, ou a métrica nunca sai.
- **Confiar em "exactly-once" e ignorar idempotência** — sob falha real, duplicatas aparecem.
- **Esquecer o estado** — agregação de janela sem checkpoint perde contagens numa queda.
- **Janela errada para a pergunta** — usar tumbling onde o negócio pede sessão (ou vice-versa).

## 💼 O que o mercado espera
Distinguir tempo de evento de processamento, escolher o tipo de janela pela pergunta, explicar
watermarks e as três semânticas de entrega — e saber que exactly-once, na prática, é at-least-once +
idempotência. Aparece em entrevistas de streaming e system design.

:::{admonition} ✨ Em resumo
:class: resumo
- Agregue por **tempo de evento** (quando ocorreu), não de processamento (quando chegou).
- **Janelas** (tumbling/sliding/session) recortam o stream infinito para agregar; **watermarks** decidem quando fechá-las.
- Entrega: **at-most / at-least / exactly-once**; na prática, **at-least-once + idempotência** ≈ exactly-once.
- Agregação de stream é **stateful** — o estado precisa de checkpoints para sobreviver a falhas.
:::

## 🧠 Quiz de recall
1. Qual a diferença entre tempo de evento e de processamento, e qual usar?
   :::{dropdown} Resposta
   Tempo de evento = quando o fato ocorreu; de processamento = quando o sistema o viu. Para métricas temporais corretas usa-se o tempo de evento, senão atrasos distorcem as agregações.
   :::
2. Para que servem janelas e cite três tipos.
   :::{dropdown} Resposta
   Recortam o stream infinito em intervalos finitos para agregar. Tipos: tumbling (fixa, sem sobreposição), sliding (deslizante, sobrepõe) e session (agrupa por atividade separada por inatividade).
   :::
3. O que é um watermark?
   :::{dropdown} Resposta
   A decisão de "já vi eventos suficientes até o tempo T, considero as janelas até T completas" — o equilíbrio entre esperar atrasados (completude) e emitir o resultado (latência).
   :::
4. Quais as três semânticas de entrega?
   :::{dropdown} Resposta
   At-most-once (pode perder, não duplica), at-least-once (não perde, pode duplicar) e exactly-once (nem perde nem duplica no resultado).
   :::
5. Como se obtém exactly-once na prática?
   :::{dropdown} Resposta
   Geralmente com at-least-once + idempotência: se reprocessar não altera o resultado (via chave/upsert/dedup), duplicatas de entrega não corrompem o estado.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você contaria eventos por minuto num stream com eventos atrasados?"
  :::{dropdown} Resposta modelo
  Agrego por **tempo de evento** em janelas **tumbling de 1 minuto**, para que um evento atrasado caia no minuto em que realmente ocorreu. Uso um **watermark** (ex.: alguns segundos) para decidir quando fechar cada janela, tolerando atrasos pequenos. Faço o resultado idempotente (sobrescrevo a contagem da janela), então reprocessamentos após falha não inflam os números.
  :::
- **P:** "O broker garante exactly-once, então não preciso me preocupar com duplicatas?"
  :::{dropdown} Resposta modelo
  Na prática, não confio nisso cegamente. Trato a entrega como at-least-once e torno o **consumidor idempotente** — chaves, upserts, dedup — para que uma duplicata não corrompa o estado. Essa combinação entrega o efeito de exactly-once de forma robusta, e é a mesma disciplina de idempotência que uso no batch (M08/M09).
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 11, tempo, janelas e garantias).
- **Documentação do Apache Flink** — tempo de evento, watermarks e exactly-once.
- **Documentação do Kafka Streams** — janelas e estado sobre tópicos Kafka.

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 11, tempo/janelas/garantias. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — transformações em streaming. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — processamento de streams. <!-- @densmore2021 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
