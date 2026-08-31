# Replicação, consistência e o teorema CAP

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você replica os dados para sobreviver a falhas (unidade 1) — agora existem **várias cópias** do mesmo
dado em máquinas diferentes. Surge a pergunta mais difícil dos sistemas distribuídos: quando alguém
**escreve** numa cópia, quando as outras enxergam a mudança? Se um cliente lê a réplica A e outro lê a
réplica B **no mesmo instante**, eles podem ver valores diferentes? Essas perguntas decidem se seu
sistema mostra saldos errados, likes que somem, ou pedidos duplicados. A resposta envolve um trade-off
inescapável — o **teorema CAP** — que todo engenheiro de dados precisa saber navegar.

## 💡 Conceito (o porquê)

### Replicação líder–seguidores
O modelo mais comum: uma réplica é o **líder** (recebe as escritas); as demais são **seguidoras** e
copiam as mudanças do líder.
- **Replicação síncrona:** o líder só confirma a escrita depois que a(s) seguidora(s) confirmaram. Mais
  segura (a cópia existe), mais lenta (espera).
- **Replicação assíncrona:** o líder confirma na hora e propaga depois. Rápida, mas cria **replication
  lag** — a seguidora fica momentaneamente **atrasada**, e uma leitura nela pode devolver dado velho.

### Consistência forte vs eventual
- **Consistência forte:** toda leitura enxerga a escrita mais recente — como se houvesse uma só cópia.
  Cômodo de programar, custa latência/disponibilidade.
- **Consistência eventual:** as réplicas **convergem** para o mesmo valor "em algum momento"; até lá,
  leituras podem ver versões diferentes. Escala e fica disponível, mas a aplicação precisa tolerar
  dados momentaneamente desatualizados (você viu isso no NoSQL, M18).

Entre os extremos há garantias intermediárias úteis (ex.: **read-your-own-writes** — você sempre vê
suas próprias escritas, mesmo que não as dos outros ainda).

### Quóruns: R + W > N
Como ter consistência **sem** um líder único e **sem** exigir todas as réplicas? Com **quóruns**. Com
N réplicas, você exige que cada escrita seja confirmada por **W** réplicas e cada leitura consulte
**R** réplicas. Se **R + W > N**, os conjuntos de escrita e de leitura **se sobrepõem** — a leitura
sempre alcança pelo menos uma réplica com o valor mais novo. É como Cassandra e Dynamo oferecem
consistência ajustável: você **escolhe** R e W conforme quer mais consistência ou mais disponibilidade.

### O teorema CAP
Num sistema distribuído, sob uma **partição de rede** (P — nós que não conseguem se comunicar, algo
inevitável), você não pode ter as duas ao mesmo tempo:
- **Consistência (C):** toda leitura vê a escrita mais recente (ou erra).
- **Disponibilidade (A):** toda requisição recebe resposta (mesmo que possivelmente desatualizada).

Sob partição, é **C ou A**: ou o sistema recusa responder para não devolver dado errado (escolhe C),
ou responde com o que tem, arriscando estar velho (escolhe A). **Não há partição? Você tem as duas.**
Por isso o CAP é sobre o que fazer **durante** falhas de rede — e por que "CP" (bancos que priorizam
consistência) e "AP" (muitos NoSQL, que priorizam disponibilidade) são escolhas de projeto, não
defeitos.

### PACELC: o trade-off também vale sem falhas
O CAP só fala de partição. O **PACELC** completa: **se** houver Partição (P), escolha entre A e C;
**senão** (Else, operação normal), escolha entre **Latência (L)** e **Consistência (C)**. Ou seja,
mesmo sem falhas, consistência forte custa latência (esperar as réplicas). É o trade-off que nunca some.

## 🔎 Exemplo
Um contador de "curtidas" usa replicação **assíncrona** e consistência **eventual** (escolha AP): se
uma réplica fica atrasada, você pode ver 999 em vez de 1000 curtidas por um instante — irrelevante
para o negócio, e o sistema nunca fica indisponível. Já o **saldo bancário** exige consistência
**forte** (escolha CP): sob partição, o sistema prefere **recusar** a transação a mostrar um saldo
errado. O mesmo sistema pode usar **quóruns** (R+W>N) para o histórico de transações, ajustando o
equilíbrio. Uma decisão de CAP por tipo de dado — não uma resposta única.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann trata **replicação** (líder/seguidores, síncrona/assíncrona, lag), os modelos de
**consistência** (forte, eventual, read-your-writes) e formaliza os trade-offs (quóruns, CAP,
linearizabilidade). — *Designing Data-Intensive Applications* (caps. 5 e 9).
:::

:::{admonition} 🏭 Do mundo real
:class: important
O CAP é frequentemente mal citado como "escolha 2 de 3". O correto: partições **acontecem** (não são
opcionais), então o design real é **como se comportar durante uma** — priorizar consistência (recusar)
ou disponibilidade (responder com o que tem). Amazon Dynamo escolheu AP (disponibilidade acima de
tudo); muitos bancos financeiros escolhem CP. — Kleppmann.
:::

## ⚠️ Erros comuns
- **Assumir que réplica está sempre atualizada** — com replicação assíncrona há lag; leitura pode ser velha.
- **Achar CAP = "escolha 2 de 3"** — é sobre C **ou** A **durante** uma partição; sem partição, tem as duas.
- **Exigir consistência forte onde não precisa** — paga latência/disponibilidade à toa (ex.: contador de likes).
- **Aceitar consistência eventual onde não pode** — saldo/estoque crítico pede consistência forte.
- **Esquecer o custo de latência** (PACELC) — consistência forte custa mesmo sem falhas.

## 💼 O que o mercado espera
Explicar replicação (síncrona/assíncrona, lag), consistência forte vs eventual, a regra de quórum
R+W>N e o teorema CAP corretamente — e escolher o trade-off por tipo de dado. Aparece em system
design e em qualquer discussão de banco distribuído.

:::{admonition} ✨ Em resumo
:class: resumo
- **Replicação** líder–seguidores; assíncrona é rápida mas cria **lag** (leitura pode ser velha).
- **Consistência forte** (toda leitura vê a última escrita) vs **eventual** (réplicas convergem depois).
- **Quórum**: com **R + W > N**, leitura e escrita se sobrepõem → consistência ajustável.
- **CAP**: sob partição, escolha **C ou A**; **PACELC**: mesmo sem partição, **latência vs consistência**.
:::

## 🧠 Quiz de recall
1. Qual a diferença entre replicação síncrona e assíncrona?
   :::{dropdown} Resposta
   Síncrona: o líder espera a seguidora confirmar antes de confirmar a escrita (mais segura, mais lenta). Assíncrona: confirma na hora e propaga depois (rápida, mas cria replication lag).
   :::
2. Consistência forte vs eventual?
   :::{dropdown} Resposta
   Forte: toda leitura vê a escrita mais recente (como cópia única). Eventual: réplicas convergem "em algum momento"; até lá, leituras podem divergir.
   :::
3. O que garante a regra R + W > N?
   :::{dropdown} Resposta
   Que os conjuntos de réplicas lidas (R) e escritas (W) se sobreponham, então a leitura sempre alcança ao menos uma réplica com o valor mais recente.
   :::
4. O que o teorema CAP realmente afirma?
   :::{dropdown} Resposta
   Sob uma partição de rede (P), você escolhe entre consistência (C: recusar para não errar) e disponibilidade (A: responder mesmo possivelmente velho). Sem partição, tem as duas.
   :::
5. O que o PACELC acrescenta ao CAP?
   :::{dropdown} Resposta
   Que mesmo sem partição (Else), há trade-off entre Latência e Consistência: consistência forte custa latência sempre.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Seu banco distribuído sofre uma partição de rede. O que você prioriza?"
  :::{dropdown} Resposta modelo
  Depende do dado. Para algo crítico (saldo, estoque), priorizo consistência (CP): prefiro recusar a operação a devolver um valor errado. Para algo tolerante (contador de likes, feed), priorizo disponibilidade (AP): respondo com o que tenho e deixo convergir depois. O CAP não é uma escolha global — é por tipo de dado e por operação, e uso quóruns (R+W>N) para ajustar onde dá.
  :::
- **P:** "Um usuário reclama que atualizou o perfil mas ainda vê o dado antigo. O que houve?"
  :::{dropdown} Resposta modelo
  Provavelmente replication lag com consistência eventual: a escrita foi para o líder, mas a leitura caiu numa seguidora ainda atrasada. A correção comum é garantir **read-your-own-writes** — rotear as leituras do próprio usuário para o líder (ou uma réplica atualizada) por um tempo após a escrita, para ele sempre ver a própria mudança.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 5 replicação, cap. 9 consistência/consenso).
- **Reis & Housley — Fundamentals of Data Engineering** (consistência em sistemas de dados).
- **Documentação do Apache Cassandra** — níveis de consistência ajustáveis (quóruns).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — replicação, CAP, consistência. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — consistência de dados. <!-- @reis2022 -->
- Dean, J.; Ghemawat, S. *MapReduce* (2004) — tolerância a falhas em cluster. <!-- @dean2004 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
