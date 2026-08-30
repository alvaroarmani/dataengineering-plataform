# Ingestão de APIs: paginação, rate limit e autenticação

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Muito dado vem de **APIs** — câmbio do Banco Central, dados do IBGE, um SaaS qualquer. Parece
simples ("é só um GET"), mas na prática você bate em: a API devolve os dados em **páginas**,
tem **limite de requisições** (rate limit), exige **autenticação**, e às vezes **falha**. Saber
ingerir uma API de forma robusta — pra baixar tudo sem ser bloqueado e sem perder dados — é
uma habilidade cobrada em quase toda vaga de DE.

## 💡 Conceito (o porquê)

### Paginação: a API não te dá tudo de uma vez
Respostas grandes vêm **fatiadas**. Dois estilos:
- **Offset/limit (ou page):** `?limit=100&offset=200` — você pede "os 100 a partir do 200".
  Simples, mas frágil se os dados mudam durante a paginação.
- **Cursor/token:** a resposta traz um `next` (um ponteiro); você repete com ele até vir vazio.
  Mais robusto para dados que mudam.

O padrão é **um laço**: busca uma página, processa, avança — até não haver mais.

### Rate limit: não seja bloqueado
APIs limitam quantas requisições você pode fazer (ex.: 60/min). Ao estourar, respondem
**HTTP 429 (Too Many Requests)**. O certo é **respeitar o limite** e, ao tomar 429/erro
transitório, **tentar de novo com espera crescente** — *retry com backoff exponencial*
(espera 1s, 2s, 4s...), idealmente com um pequeno *jitter* (aleatório) para não sincronizar.

### Autenticação
Formas comuns de a API te identificar:
- **API key** (num header `Authorization` ou query param).
- **Bearer token** (`Authorization: Bearer <token>`), às vezes obtido via **OAuth**.
- APIs **públicas** (Banco Central, IBGE) muitas vezes não exigem chave.
> A chave é **segredo**: nunca commite; use variável de ambiente.

### Incremental via API
Boas APIs aceitam um filtro de data (`?since=2026-08-01` ou intervalo). Aí a **marca d'água**
(U1) vale igual: guarde a última data ingerida e peça só o que veio depois.

### Robustez
- **Timeout** em toda requisição (nunca "pendure" para sempre).
- **Trate erros**: 4xx (seu pedido) vs 5xx/429 (tente de novo).
- **Idempotência** na escrita (upsert) — reprocessar uma página não duplica.

## 🔎 Exemplo
Baixar uma série do **Banco Central (SGS)**: um `GET` retorna JSON com N registros. Se a série
for grande, você pagina por intervalo de datas; se tomar 429, espera e repete; salva no
Postgres com upsert por data. Guarda a última data como marca d'água para amanhã trazer só o novo.

:::{admonition} 📖 Da literatura
:class: seealso
Densmore trata a ingestão de APIs como padrão central: paginar até esgotar, respeitar limites
com retries/backoff, autenticar com segredos fora do código, e escrever de forma idempotente —
os pilares de um extrator confiável. — *Data Pipelines Pocket Reference*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
APIs públicas brasileiras são ótimas para praticar: o **SGS do Banco Central**
(`dadosabertos.bcb.gov.br`) e o **IBGE** (`servicodados.ibge.gov.br`) entregam JSON sem chave.
Ver o lab desta unidade e `datasets/README.md`.
:::

## ⚠️ Erros comuns
- **Ignorar a paginação** — você baixa só a primeira página e acha que tem tudo.
- **Não tratar 429/erros** — o job quebra ou te bloqueiam; falta retry com backoff.
- **Sem timeout** — uma requisição travada pendura o pipeline.
- **Commitar a chave** da API — vazamento de segredo; use env var.
- Reprocessar sem **idempotência** — páginas repetidas duplicam dados.

## 💼 O que o mercado espera
Extrair de uma API real com paginação, rate limit e estado (incremental) é o **exercício de
maestria** deste módulo e cai direto em entrevista ("como você baixaria toda a série de uma API
que pagina e limita requisições?").

:::{admonition} ✨ Em resumo
:class: resumo
- APIs entregam em **páginas** (offset/limit ou cursor) — pagine num laço até esgotar.
- Respeite o **rate limit**; em 429/erro transitório, **retry com backoff exponencial** (+jitter).
- **Autentique** com segredo fora do código (env var); muitas APIs públicas não exigem chave.
- Combine com **marca d'água** (incremental) e **upsert** (idempotência); use **timeout** sempre.
:::

## 🧠 Quiz de recall
1. Cite os dois estilos de paginação e a diferença.
   :::{dropdown} Resposta
   Offset/limit (pede um intervalo por posição; simples, frágil se os dados mudam) e cursor/token (a resposta traz um next; repete até vir vazio; robusto).
   :::
2. O que é HTTP 429 e como reagir?
   :::{dropdown} Resposta
   "Too Many Requests" — você estourou o rate limit. Reaja com retry e backoff exponencial (espera crescente, +jitter), respeitando o limite.
   :::
3. Onde NÃO colocar a chave da API?
   :::{dropdown} Resposta
   No código/commit. Use variável de ambiente; a chave é segredo.
   :::
4. Como fazer ingestão incremental de uma API?
   :::{dropdown} Resposta
   Usando um filtro de data (ex.: ?since=) e uma marca d'água: guarda a última data ingerida e pede só o que veio depois.
   :::
5. Por que sempre usar timeout?
   :::{dropdown} Resposta
   Para não "pendurar" o pipeline indefinidamente se a API não responder; a requisição falha rápido e você trata/reintenta.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você baixaria toda a série de uma API que pagina e limita requisições?"
  :::{dropdown} Resposta modelo
  Um laço de paginação (offset/limit ou seguindo o cursor next) até esgotar; timeout em cada request; ao tomar 429/5xx, retry com backoff exponencial e jitter respeitando o limite; autentico com a chave vinda de env var; escrevo com upsert (idempotente) e guardo a marca d'água para a próxima carga ser incremental.
  :::
- **P:** "Sua ingestão de API às vezes duplica dados. O que pode ser?"
  :::{dropdown} Resposta modelo
  Reprocessamento de páginas sem idempotência. Resolvo com upsert por chave natural e/ou controle de estado (marca d'água) para não repetir intervalos já ingeridos.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Densmore — Data Pipelines Pocket Reference** (extração de APIs, paginação, retries).
- **Banco Central (SGS)** e **IBGE** — APIs públicas para praticar (ver o lab desta unidade).

## 📚 Referências
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — ingestão de APIs (paginação, rate limit, idempotência). <!-- @densmore2021 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — ingestão a partir de APIs. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
