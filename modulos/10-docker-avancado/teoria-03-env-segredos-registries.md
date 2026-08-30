# Variáveis de ambiente, segredos, reprodutibilidade e registries

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Falta o que torna um container **configurável e seguro** de verdade: como passar configuração
sem recompilar a imagem, como **não vazar segredos** (senha do banco, token da API), como
garantir que a imagem de hoje é **idêntica** à de amanhã, e como **compartilhar** a imagem
(registry). Errar aqui vaza credenciais e cria os clássicos "funciona só aqui".

## 💡 Conceito (o porquê)

### Configuração via variáveis de ambiente
A mesma imagem roda em dev/prod mudando só as **variáveis de ambiente** — a config **não** vai
"queimada" na imagem. No Compose:
```yaml
environment:
  POSTGRES_HOST: "${POSTGRES_HOST:-postgres}"   # usa a env; se ausente, default 'postgres'
```
A sintaxe **`${VAR:-default}`** resolve para o valor de `VAR` ou, se vazio/ausente, o
`default`. Um arquivo **`.env`** (não versionado) fornece esses valores localmente.

### Segredos: o que NUNCA fazer
- **Nunca** faça `ENV SENHA=...` nem `COPY .env` para dentro da imagem — fica **gravado nas
  camadas** (qualquer um que puxe a imagem lê). Segredo em `Dockerfile`/imagem = vazamento.
- Passe segredos em **runtime** (variáveis de ambiente injetadas, Docker/Compose secrets, ou o
  cofre da plataforma). O `.env` fica **no `.gitignore`**; versione só um `.env.example` sem valores.
- Isso ecoa o M9 (Connections/Variables do Airflow) e a plataforma (a `anon key` pública vs a
  `service_role` secreta).

### Reprodutibilidade: pinar tudo
"Funciona hoje" tem que continuar funcionando. **Pine versões**: a imagem base
(`python:3.12-slim`, não `python:latest`), as dependências (lockfile), e a tag da imagem que
você publica. `latest` é um alvo móvel — evite em produção.

### Registries: onde as imagens vivem
Uma imagem construída é **publicada** num **registry** para ser puxada em outro lugar:
- **Docker Hub** (`docker.io`, padrão), **GHCR** (`ghcr.io`), registries de cloud (ECR/GCR/ACR).
- Fluxo: `docker build -t ghcr.io/voce/app:1.2.0 .` → `docker push ghcr.io/voce/app:1.2.0`.
- Uma referência de imagem é `registry/nome:tag` (sem registry → `docker.io`; sem tag → `latest`).

## 🔎 Exemplo
A bancada usa `${POSTGRES_PASSWORD:-curso}` vindo do `.env` (que está no `.gitignore`); só o
`.env.example` é versionado. As imagens são **pinadas** (`postgres:16.4`, `apache/airflow:2.10.3`).
Para compartilhar a imagem do seu pipeline, você a taggeia como `ghcr.io/voce/pipeline:1.0.0`
e faz `push` — em qualquer máquina, `docker pull` traz exatamente aquela versão.

:::{admonition} 📖 Da literatura
:class: seealso
A documentação do Docker recomenda configurar via variáveis de ambiente, **manter segredos fora
da imagem** (eles persistem nas camadas), pinar versões para reprodutibilidade e publicar
imagens versionadas em registries — o ciclo build → tag → push → pull. — Docker, docs oficiais.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Vazamento de segredo em imagem/`Dockerfile` é um incidente comum e sério — a camada guarda o
valor mesmo que você "apague" depois. Times escaneiam imagens por segredos e pinam versões +
registry privado como padrão. — Docker, docs oficiais.
:::

## ⚠️ Erros comuns
- **Segredo na imagem** (`ENV SENHA=...`, `COPY .env`) — fica nas camadas; vazamento.
- Usar **`latest`** em produção — build não reprodutível; pinar a tag.
- Commitar o **`.env`** — versione só `.env.example` sem valores.
- Config "queimada" na imagem em vez de via env — obriga rebuild para cada ambiente.
- Não versionar a tag da imagem publicada — impossível saber o que está rodando.

## 💼 O que o mercado espera
Gerir configuração por env, **manter segredos fora da imagem**, pinar versões e publicar em
registry é higiene básica de quem entrega containers. Vazar segredo ou depender de `latest` são
red flags em code review.

:::{admonition} ✨ Em resumo
:class: resumo
- Configure por **variáveis de ambiente** (`${VAR:-default}` + `.env` ignorado); config fora da imagem.
- **Segredos nunca na imagem/Dockerfile** (persistem nas camadas) — injete em runtime; versione só `.env.example`.
- **Reprodutibilidade:** pine base, dependências e a **tag** publicada; evite `latest` em produção.
- **Registry:** `build → tag (registry/nome:tag) → push → pull`; sem registry = docker.io, sem tag = latest.
:::

## 🧠 Quiz de recall
1. O que faz `${POSTGRES_HOST:-postgres}`?
   :::{dropdown} Resposta
   Resolve para o valor da variável POSTGRES_HOST; se ausente/vazia, usa o default 'postgres'.
   :::
2. Por que NÃO colocar segredo no Dockerfile/imagem?
   :::{dropdown} Resposta
   Porque fica gravado nas camadas da imagem — qualquer um que a puxe consegue ler, mesmo que você "apague" depois. Segredos vão em runtime (env/secrets), e o .env fica no .gitignore.
   :::
3. Por que evitar `latest` em produção?
   :::{dropdown} Resposta
   É um alvo móvel: a imagem pode mudar sem aviso, quebrando a reprodutibilidade. Pine uma tag específica.
   :::
4. O que é um registry e o fluxo de publicação?
   :::{dropdown} Resposta
   Onde as imagens são armazenadas/compartilhadas (Docker Hub, GHCR, ECR...). Fluxo: build -t registry/nome:tag → push → (em outra máquina) pull.
   :::
5. Como se lê `ghcr.io/voce/app:1.2.0`?
   :::{dropdown} Resposta
   registry = ghcr.io, nome = voce/app, tag = 1.2.0. Sem registry, assume docker.io; sem tag, assume latest.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você passa a senha do banco para um container sem vazá-la?"
  :::{dropdown} Resposta modelo
  Nunca na imagem/Dockerfile (persiste nas camadas). Passo em runtime: variável de ambiente injetada, Docker/Compose secrets, ou o cofre da plataforma. O `.env` fica no `.gitignore`; versiono só um `.env.example`.
  :::
- **P:** "Como garantir que a imagem de hoje roda igual daqui a seis meses?"
  :::{dropdown} Resposta modelo
  Pinando tudo: base com tag fixa (não `latest`), dependências via lockfile, e publicando a imagem com uma tag versionada (ex.: 1.2.0) num registry — assim `pull` traz exatamente aquela versão.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Docker docs** — *Environment variables*, *Manage secrets*, *Sharing images (registries)*.

## 📚 Referências
- Docker — Documentação oficial (env vars, secrets, registries, reprodutibilidade). <!-- @docs-docker -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — segurança e reprodutibilidade. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
