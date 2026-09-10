# Resiliência na integração: idempotência, retry e Saga

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Integração distribuída **falha o tempo todo**: a rede cai no meio de uma chamada, uma mensagem é
entregue duas vezes, um serviço fica lento, uma transação atravessa três serviços e o terceiro
recusa. Se cada falha dessas corromper dados (cobrar duas vezes, estoque negativo, pedido "meio
criado"), o sistema é inútil. A diferença entre um integrador amador e um profissional está nos
**padrões de resiliência** — idempotência, retry com backoff, e Saga — que fazem o sistema **se
recuperar sozinho** sem duplicar nem corromper. São os mesmos princípios da idempotência que você já
viu (M08/M09/M17), agora como um kit de integração.

## 💡 Conceito (o porquê)

### Idempotência: reprocessar sem estragar
Uma operação é **idempotente** quando executá-la **N vezes tem o mesmo efeito que uma vez**. É a
propriedade mais importante da integração confiável, porque as garantias de entrega são quase sempre
**at-least-once** (M17): mensagens/chamadas se repetem após falha. Como garantir:
- **Idempotency-Key:** o cliente manda uma chave única por requisição; o servidor, se já viu a chave,
  **retorna o resultado anterior** em vez de reprocessar (não cobra duas vezes).
- **Upsert por chave natural** (M08): inserir-ou-atualizar em vez de só inserir.
Com idempotência, retry e reentrega deixam de ser perigosos.

### Retry com backoff exponencial
Falhas **transitórias** (5xx, timeout, rede) pedem **retry** — mas repetir imediatamente e em rajada
piora as coisas (martela um serviço já sobrecarregado). O padrão é **backoff exponencial**: espere
mais a cada tentativa (ex.: 1s, 2s, 4s, 8s…), idealmente com um **jitter** (aleatoriedade) para não
sincronizar todos os clientes. E só faça retry no que é **retriável** (5xx/timeout), nunca num
`400/404` (unidade 1) — reenviar uma requisição inválida nunca vai dar certo.

### Circuit breaker: parar de bater na porta
Se um serviço está claramente fora (falhas seguidas), continuar tentando desperdiça recursos e
propaga a lentidão. O **circuit breaker** "abre" após N falhas: para de chamar por um tempo, deixa o
serviço respirar, e testa de novo depois. Protege o chamador de ficar preso e o chamado de ser
soterrado — evita o **efeito dominó** entre microserviços.

### Saga: transações que cruzam serviços
Uma compra toca **vários** serviços (reservar estoque → cobrar → enviar). Não existe um `COMMIT`
único entre bancos diferentes (não há transação ACID distribuída simples). O padrão **Saga** resolve:
a transação vira uma **sequência de passos locais**, cada um com uma **ação compensatória** que o
desfaz. Se um passo falha, executam-se as compensações dos passos já concluídos **na ordem inversa** —
"desfazer" o que foi feito, deixando o sistema consistente.
- Ex.: concluiu `reservar` e `cobrar`, mas `enviar` falhou → compense na ordem inversa: `estornar`
  (desfaz cobrar) e `liberar` (desfaz reservar).
É consistência **eventual** coordenada por compensações, no lugar de um rollback atômico.

### Observabilidade da integração
Como saber que tudo isso está funcionando? Com **observabilidade** (M12): logs correlacionados por um
**trace id** que segue a requisição por todos os serviços, métricas de latência/erro por serviço, e
alertas. Numa arquitetura distribuída, sem rastreamento você fica cego sobre onde a falha aconteceu.

## 🔎 Exemplo
Um pagamento chega duas vezes (a rede reentregou). O serviço usa a **Idempotency-Key** da requisição:
a segunda vez, reconhece a chave e devolve o resultado da primeira — **não cobra de novo**. Uma
chamada ao antifraude dá timeout (5xx): o cliente faz **retry com backoff** (1s, 2s, 4s); após 5
falhas seguidas, o **circuit breaker** abre e para de tentar por 30s. Já a compra inteira é uma
**Saga**: reservou estoque e cobrou, mas o envio falhou → o sistema **estorna** e **libera o estoque**
(compensações na ordem inversa), deixando tudo consistente. Um **trace id** amarra todos esses passos
nos logs. Falhas aconteceram; dados permaneceram corretos.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann trata **entrega at-least-once e idempotência**, os limites das transações distribuídas e as
abordagens de consistência por compensação — o fundamento por trás de retries e Sagas. Reis & Housley
reforçam idempotência e observabilidade como *undercurrents* de pipelines confiáveis. — *Designing
Data-Intensive Applications* (cap. 9 e 11); *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
"Exactly-once" de verdade quase não existe na integração; o que existe é **at-least-once +
idempotência**. Sistemas de pagamento sérios usam Idempotency-Key exatamente para não cobrar em
dobro quando o cliente reenviar. E Saga é o padrão de fato para "transações" que cruzam
microserviços, porque não há COMMIT distribuído simples. — Kleppmann; prática de mercado.
:::

## ⚠️ Erros comuns
- **Retry sem idempotência** — reprocessar duplica (cobra duas vezes, insere repetido).
- **Retry imediato/em rajada** — martela um serviço já caído; use backoff exponencial (+ jitter).
- **Retry no 4xx** — reenviar requisição inválida nunca resolve; só retriar 5xx/timeout.
- **Transação distribuída "atômica"** entre serviços — não existe simples; use Saga com compensações.
- **Sem trace id/observabilidade** — numa falha distribuída, você fica cego sobre onde quebrou.

## 💼 O que o mercado espera
Aplicar idempotência (Idempotency-Key/upsert), retry com backoff (só no retriável), noção de circuit
breaker, e explicar Saga (compensações na ordem inversa) para transações entre serviços — além de
observabilidade com trace id. É o núcleo de qualquer discussão séria de integração/system design.

:::{admonition} ✨ Em resumo
:class: resumo
- **Idempotência** (Idempotency-Key / upsert) torna retry e reentrega seguros — a garantia é at-least-once.
- **Retry com backoff exponencial** (+ jitter), só no **retriável** (5xx/timeout), nunca no 4xx.
- **Circuit breaker** para de chamar um serviço caído, evitando o efeito dominó.
- **Saga**: transação entre serviços = passos locais + **compensações na ordem inversa** (não há COMMIT distribuído).
:::

## 🧠 Quiz de recall
1. Por que idempotência é central na integração?
   :::{dropdown} Resposta
   Porque a entrega é at-least-once: mensagens/chamadas se repetem após falha. Se a operação é idempotente (N vezes = 1 vez), retry e reentrega não duplicam nem corrompem.
   :::
2. Como funciona o retry com backoff exponencial e quando aplicá-lo?
   :::{dropdown} Resposta
   Espera-se mais a cada tentativa (1s, 2s, 4s…), idealmente com jitter, e só em falhas retriáveis (5xx/timeout) — nunca em 4xx (requisição inválida).
   :::
3. O que faz um circuit breaker?
   :::{dropdown} Resposta
   Após N falhas seguidas, "abre" e para de chamar o serviço por um tempo, deixando-o respirar e evitando o efeito dominó; depois testa de novo.
   :::
4. O que é o padrão Saga?
   :::{dropdown} Resposta
   Uma transação entre serviços feita de passos locais, cada um com uma ação compensatória; se um passo falha, executam-se as compensações dos passos concluídos na ordem inversa, restaurando a consistência.
   :::
5. Por que uma Idempotency-Key evita cobrança dupla?
   :::{dropdown} Resposta
   Porque o servidor guarda a chave da requisição; ao ver a mesma chave de novo, retorna o resultado anterior em vez de reprocessar o pagamento.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você garante que um pagamento não seja cobrado duas vezes numa integração?"
  :::{dropdown} Resposta modelo
  Idempotência via Idempotency-Key: o cliente envia uma chave única por requisição; o serviço registra a chave e, se ela reaparecer (reentrega/retry), devolve o resultado da primeira execução sem cobrar de novo. Combino com retry só em falhas retriáveis (5xx/timeout) com backoff, e trato a operação como at-least-once. É a mesma disciplina de idempotência dos pipelines (M08/M09).
  :::
- **P:** "Uma compra passa por estoque, pagamento e envio, em serviços diferentes. Como manter consistência?"
  :::{dropdown} Resposta modelo
  Com uma Saga: cada passo é uma transação local (reservar estoque, cobrar, enviar), e cada um tem uma compensação (liberar, estornar, cancelar envio). Se um passo falha, executo as compensações dos passos já concluídos na ordem inversa, deixando o sistema consistente — porque não existe COMMIT atômico entre bancos diferentes. Amarro tudo com um trace id para observar o fluxo.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 9 e 11, idempotência/consistência).
- **Reis & Housley — Fundamentals of Data Engineering** (idempotência e observabilidade).
- **Documentação sobre Saga pattern e Idempotency-Key** (ex.: guias de pagamentos/Stripe).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — idempotência, consistência, compensação. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — idempotência e observabilidade. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — resiliência em pipelines. <!-- @densmore2021 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
