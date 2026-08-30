# Dockerfile avançado: camadas, cache e imagens enxutas

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Você já usou a bancada Docker (M2) e subiu Postgres/Airflow/dbt. Agora vem o outro lado:
**empacotar o seu próprio código** numa imagem — de forma que o build seja **rápido** (cache) e
a imagem **pequena** (deploy leve, menos superfície de ataque). Um `Dockerfile` mal escrito
gera imagens de 2 GB que rebuildam do zero a cada mudança; um bom, imagens enxutas que
aproveitam cache. Essa diferença é cobrada em vaga e sentida todo dia.

## 💡 Conceito (o porquê)

### Imagem, camadas e cache
Uma imagem é feita de **camadas** empilhadas — **cada instrução** do `Dockerfile` (`FROM`,
`COPY`, `RUN`...) cria uma. O Docker **cacheia** cada camada: se nada mudou até ali, ele
reaproveita. **A regra de ouro:** a partir da **primeira instrução cujo contexto mudou**, todas
as camadas seguintes são **reconstruídas**. Por isso a ordem importa.

### Ordene do que muda menos para o que muda mais
O código-fonte muda a toda hora; as dependências, quase nunca. Então **copie e instale as
dependências antes** de copiar o código:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .          # muda raramente
RUN pip install -r requirements.txt   # camada cara — fica em cache
COPY . .                         # muda a cada commit (invalida só daqui pra baixo)
CMD ["python", "main.py"]
```
Assim, mudar o código **não** re-instala as dependências (a camada do `pip` continua em cache).
Se você fizesse `COPY . .` antes do `pip install`, cada mudança de código refaria a instalação.

### Imagens enxutas
- **Base slim/alpine:** `python:3.12-slim` ≪ `python:3.12`.
- **Multi-stage build:** um estágio "builder" (compila/instala) e um estágio final que **copia
  só o necessário** — o resultado não carrega compiladores e caches:
  ```dockerfile
  FROM python:3.12 AS builder
  RUN pip install --prefix=/inst -r requirements.txt
  FROM python:3.12-slim
  COPY --from=builder /inst /usr/local
  COPY . .
  ```
- **`.dockerignore`:** exclui do **contexto de build** o que não precisa ir (`.git`,
  `node_modules`, `__pycache__`, `.env`) — build mais rápido e imagem/contexto menor.

### Cada camada é imutável (e some no cache errado)
Combinar comandos relacionados num `RUN` (com limpeza no fim) reduz camadas e tamanho:
`RUN apt-get update && apt-get install -y X && rm -rf /var/lib/apt/lists/*`.

## 🔎 Exemplo
Um serviço Python: com `COPY requirements.txt` + `pip install` **antes** do `COPY . .`, um
commit que muda só `main.py` rebuilda em segundos (reusa a camada do pip). Com multi-stage +
base slim, a imagem cai de ~1 GB para ~150 MB. O `.dockerignore` evita mandar o `.git` de
500 MB para o contexto.

:::{admonition} 📖 Da literatura
:class: seealso
A documentação do Docker organiza as *best practices* de Dockerfile em torno de **camadas e
cache** (ordenar do estável ao volátil), **multi-stage builds** para imagens enxutas e
**`.dockerignore`** para um contexto pequeno — os pilares de builds rápidos e imagens leves. —
Docker, documentação oficial (best practices).
:::

:::{admonition} 🏭 Do mundo real
:class: important
Imagens enormes são um problema real: mais lentas para puxar/subir, mais caras de armazenar e
com maior superfície de ataque. Times padronizam bases slim, multi-stage e `.dockerignore` — e
medem o tamanho da imagem no CI. — Docker, docs oficiais.
:::

## ⚠️ Erros comuns
- **`COPY . .` antes de instalar dependências** — cada mudança de código re-instala tudo (cache perdido).
- **Base "cheia"** (`python:3.12`) quando `-slim` bastava — imagem gigante.
- Não usar **multi-stage** — compiladores/caches vão para a imagem final.
- **Sem `.dockerignore`** — manda `.git`/`node_modules` para o contexto; build lento.
- Vários `RUN apt-get` sem `rm -rf /var/lib/apt/lists/*` — camadas e lixo acumulados.

## 💼 O que o mercado espera
Escrever um `Dockerfile` que aproveita cache e gera imagem enxuta (multi-stage, slim,
`.dockerignore`) é requisito recorrente. "Por que seu build está lento / sua imagem está
gigante?" é pergunta clássica — e a resposta é ordem de camadas + multi-stage.

:::{admonition} ✨ Em resumo
:class: resumo
- Cada instrução vira uma **camada**; o Docker **cacheia** — a partir da 1ª que mudou, tudo rebuilda.
- **Ordene do estável ao volátil:** dependências antes do código (`COPY requirements` + `pip` antes de `COPY . .`).
- Imagens enxutas: **base slim**, **multi-stage** (copia só o necessário), **`.dockerignore`**.
- Agrupe `RUN` relacionados com limpeza para menos camadas/tamanho.
:::

## 🧠 Quiz de recall
1. O que é uma camada e como funciona o cache?
   :::{dropdown} Resposta
   Cada instrução do Dockerfile cria uma camada; o Docker reaproveita (cacheia) as camadas até a primeira cujo contexto mudou — dali pra baixo, tudo é reconstruído.
   :::
2. Por que copiar `requirements.txt` e instalar antes de `COPY . .`?
   :::{dropdown} Resposta
   Porque dependências mudam raramente e o código muda sempre; assim a camada cara do `pip install` fica em cache e mudanças de código não a invalidam.
   :::
3. O que é um multi-stage build e o que ele resolve?
   :::{dropdown} Resposta
   Um estágio builder compila/instala e o estágio final copia só o necessário — a imagem final não carrega compiladores/caches, ficando enxuta.
   :::
4. Para que serve o `.dockerignore`?
   :::{dropdown} Resposta
   Excluir arquivos do contexto de build (.git, node_modules, __pycache__, .env) — build mais rápido, contexto e imagem menores, e evita vazar segredos.
   :::
5. Como reduzir o tamanho da imagem?
   :::{dropdown} Resposta
   Base slim/alpine, multi-stage, .dockerignore e agrupar RUN com limpeza (rm -rf caches).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Seu build Docker está lento a cada commit. O que você muda?"
  :::{dropdown} Resposta modelo
  Reordeno o Dockerfile para instalar dependências antes de copiar o código (`COPY requirements.txt` + `pip install` antes de `COPY . .`), para o cache da camada de dependências sobreviver às mudanças de código. Também adiciono `.dockerignore` para reduzir o contexto.
  :::
- **P:** "Como você deixaria a imagem menor?"
  :::{dropdown} Resposta modelo
  Base slim, multi-stage build (copiando só os artefatos necessários do estágio builder), `.dockerignore`, e agrupando `RUN` com limpeza de caches. Meço o tamanho antes/depois.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Docker docs** — *Best practices for writing Dockerfiles*, *Multi-stage builds*, *.dockerignore*.

## 📚 Referências
- Docker — Documentação oficial (Dockerfile best practices, multi-stage, .dockerignore). <!-- @docs-docker -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — reprodutibilidade e empacotamento. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
