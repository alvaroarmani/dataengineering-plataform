# APIs REST para dados: consumir e servir

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Dados raramente chegam num CSV limpo. Muitas vezes eles estão **atrás de uma API** — a cotação do
Banco Central, os pedidos de um ERP, os eventos de um SaaS. E, do outro lado, o resultado do seu
pipeline (um score, um agregado) frequentemente precisa ser **servido** para uma aplicação consumir —
não adianta ficar só numa tabela. Em ambos os casos, o engenheiro de dados fala **HTTP/REST**:
sabe paginar uma API para ingerir sem estourar limites, interpretar status codes, e expor dados de
forma confiável. Não dominar isso trava metade das integrações reais. A FIAP trata "APIs e
integração" como matéria própria — e com razão.

## 💡 Conceito (o porquê)

### REST em uma frase
Uma **API REST** expõe **recursos** (coisas: `/pedidos`, `/clientes/42`) que você manipula com
**verbos HTTP**:
- **GET** (ler), **POST** (criar), **PUT/PATCH** (atualizar), **DELETE** (remover).
- O endereço identifica o recurso; o verbo diz a ação. `GET /pedidos/42` = "leia o pedido 42".

A resposta traz um **corpo** (geralmente JSON) e um **status code** que diz o que aconteceu.

### Status codes: o resultado em um número
O status é a primeira coisa que seu código deve checar:
- **2xx — sucesso:** `200` OK, `201` Created (criou), `204` No Content (ok, sem corpo).
- **4xx — erro do cliente (você):** `400` Bad Request (payload inválido), `401` Unauthorized (sem
  credencial), `404` Not Found. **Não adianta repetir igual** — conserte a requisição.
- **5xx — erro do servidor (do outro lado):** `500`, `503`. Aqui **retry faz sentido** (o servidor
  pode se recuperar).

Essa distinção 4xx×5xx guia sua lógica de resiliência (unidade 3): retry no 5xx, corrigir no 4xx.

### Paginação: ingerir sem estourar
Nenhuma API devolve 10 milhões de linhas numa resposta. Ela **pagina**: você pede em blocos
(`?page=3&size=100` ou por cursor). Ingerir de uma API = **percorrer as páginas** até acabar. Ignorar
isso te dá só a primeira página (bug silencioso clássico) ou estoura timeouts/limites. Paginar é a
diferença entre "puxei os dados" e "puxei os primeiros 100".

### Autenticação e rate limits
APIs exigem **credenciais** (API key, token OAuth — no header, nunca na URL, M14) e impõem **rate
limits** (X requisições por minuto). O ingestor respeita o limite (throttle) e trata o `429 Too Many
Requests` recuando. Credenciais vão em **variável de ambiente/secret**, jamais no código.

### Servir dados (o outro lado)
O resultado do pipeline muitas vezes precisa ser **exposto** para consumo em tempo real (um app que
pergunta "qual o score deste cliente?"). Aí você **serve** os dados por uma API — com contratos
claros (quais campos, quais tipos), paginação, e status codes corretos. É a fronteira entre o mundo
analítico (batch) e o operacional (uma requisição por vez).

### Contrato da API
Toda API tem um **contrato**: os campos obrigatórios, seus tipos, o formato. Validar o payload contra
o contrato (campos obrigatórios presentes, tipos certos) **na borda** evita que lixo entre no
pipeline — a mesma disciplina dos data contracts (M12), aplicada à porta de entrada HTTP.

## 🔎 Exemplo
Seu ingestor puxa pedidos de um ERP via `GET /pedidos?page=N&size=200` com um token no header. O
código: valida o status (2xx segue, 429/5xx faz retry com espera, 4xx aborta e loga), percorre as
páginas até vir uma vazia, e valida cada registro contra o contrato (campos obrigatórios) antes de
gravar. Do outro lado, o time de risco expõe o resultado por `GET /clientes/42/score`, respondendo
`200` com o score em JSON, `404` se o cliente não existe. Ingestão robusta de um lado, serving
confiável do outro — tudo HTTP.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley colocam a **ingestão via APIs** (com paginação, autenticação e rate limits) entre os
padrões centrais do estágio de ingestão. Kleppmann discute REST e RPC como estilos de comunicação
entre serviços e a importância dos contratos/encoding entre eles. — *Fundamentals of Data
Engineering*; *Designing Data-Intensive Applications* (cap. 4).
:::

:::{admonition} 🏭 Do mundo real
:class: important
O bug de ingestão mais comum: pegar só a **primeira página** por não paginar, e o pipeline "funciona"
com dados incompletos por semanas. O segundo: não distinguir 4xx de 5xx e ou desistir cedo demais ou
martelar um endpoint que nunca vai responder. Paginar sempre e tratar status por classe resolve a
maioria. — Reis & Housley.
:::

## ⚠️ Erros comuns
- **Não paginar** — ingere só a primeira página; dados incompletos silenciosos.
- **Ignorar o status code** — tratar erro como sucesso (grava lixo) ou não fazer retry no 5xx.
- **Retry cego no 4xx** — martelar um endpoint com requisição inválida; conserte, não repita.
- **Credencial na URL/código** — vaza em logs/histórico; use header + secret (M14).
- **Ignorar rate limits** — tomar 429 e ser bloqueado; respeite o limite (throttle/backoff).

## 💼 O que o mercado espera
Consumir APIs (paginação, auth, rate limit, tratar status), e ter noção de **servir** dados por uma
API com contrato. "Como você ingeriria dados de uma API paginada com rate limit?" é pergunta comum
de ingestão.

:::{admonition} ✨ Em resumo
:class: resumo
- **REST**: recursos (`/pedidos/42`) + verbos (GET/POST/PUT/DELETE); a resposta traz JSON + **status code**.
- **Status por classe**: 2xx ok, **4xx corrija** (não repita), **5xx faça retry**.
- **Pagine** para ingerir tudo; respeite **auth** (header/secret) e **rate limits** (429 → recue).
- Ao **servir** dados, defina o **contrato** (campos/tipos) e valide o payload na borda.
:::

## 🧠 Quiz de recall
1. O que são recursos e verbos numa API REST?
   :::{dropdown} Resposta
   Recursos são as entidades no endereço (/pedidos/42); verbos HTTP dizem a ação (GET ler, POST criar, PUT/PATCH atualizar, DELETE remover).
   :::
2. Qual a diferença entre 4xx e 5xx, e o que ela implica?
   :::{dropdown} Resposta
   4xx é erro do cliente (payload/credencial inválidos) — conserte, não repita; 5xx é erro do servidor — retry faz sentido, pois pode se recuperar.
   :::
3. Por que paginar ao ingerir de uma API?
   :::{dropdown} Resposta
   Porque a API devolve os dados em blocos; sem percorrer as páginas você pega só a primeira (dados incompletos) ou estoura limites/timeouts.
   :::
4. Onde vão as credenciais de uma API?
   :::{dropdown} Resposta
   Em um header de autenticação, com o valor vindo de variável de ambiente/secret — nunca na URL nem no código (vaza em logs/histórico).
   :::
5. O que é o contrato de uma API e por que validá-lo?
   :::{dropdown} Resposta
   Os campos obrigatórios, tipos e formato esperados; validar na borda impede que dados inválidos entrem no pipeline (data contract na porta HTTP).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você ingeriria dados de uma API paginada com rate limit e autenticação?"
  :::{dropdown} Resposta modelo
  Autentico com token no header (vindo de secret). Percorro as páginas (page/size ou cursor) até vir vazia, respeitando o rate limit (throttle; ao tomar 429, recuo com backoff). Trato status por classe: 2xx sigo, 5xx faço retry com backoff, 4xx aborto e logo (requisição inválida). Valido cada registro contra o contrato antes de gravar, e a carga é idempotente para poder reprocessar sem duplicar.
  :::
- **P:** "Seu pipeline ingere de uma API mas os números vêm sempre incompletos. O que investigar?"
  :::{dropdown} Resposta modelo
  Quase certo que não está paginando — pega só a primeira página. Confiro se percorro todas as páginas até o fim (cursor/`has_next`), se não estou batendo em rate limit (429) e parando cedo, e se algum 5xx está sendo engolido como sucesso. Paginação + tratamento de status por classe resolve a maioria desses casos.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (ingestão via APIs).
- **Kleppmann — Designing Data-Intensive Applications** (cap. 4, comunicação entre serviços/encoding).
- **MDN — HTTP status codes** e documentação de REST.

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — ingestão por APIs. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — REST/RPC e encoding. <!-- @kleppmann2017 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — ingestão de APIs. <!-- @densmore2021 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
