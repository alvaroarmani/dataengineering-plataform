# Docker e containers: "na minha máquina funciona" nunca mais

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

A frase mais temida da engenharia: **"na minha máquina funciona"**. Seu pipeline roda no seu notebook,
mas quebra no do colega ou no servidor — versões de Python diferentes, uma biblioteca faltando, o
Postgres que era 14 lá e 16 aqui. Reproduzir um ambiente à mão é lento e frágil. **Docker** resolve
empacotando a aplicação **com todo o seu ambiente** (SO base, runtime, bibliotecas, config) numa unidade
portátil — o **container** — que roda **igual** em qualquer lugar. É por isso que a bancada do curso é um
`docker compose up`: você sobe Postgres, MinIO, dbt, Airflow e Spark idênticos aos deste material, sem
instalar nada na sua máquina. Docker é a base do ambiente reprodutível e o degrau para Kubernetes (M20).

## 💡 Conceito (o porquê)

### Imagem × container × volume (o trio essencial)
- **Imagem:** o **molde** — um pacote **imutável** e versionado com tudo que a aplicação precisa (ex.:
  `postgres:16.4`). Você a baixa de um registro (Docker Hub) ou a constrói com um `Dockerfile`.
- **Container:** uma **instância em execução** de uma imagem — o "processo" isolado rodando. De uma
  imagem você sobe **vários** containers iguais; ao parar, o container some (é efêmero).
- **Volume:** o **armazenamento persistente** que sobrevive ao container. Como o container é efêmero, os
  dados de um banco precisam ir para um **volume** — senão somem quando o container é recriado.

Analogia: a **imagem** é a receita, o **container** é o prato feito (e você faz quantos quiser), o
**volume** é a geladeira onde guarda o que não pode estragar.

### Por que containers (e não uma VM)?
Um container **compartilha o kernel** do sistema host e isola só a aplicação — então é **leve** (MB,
sobe em segundos), ao contrário de uma máquina virtual, que emula um SO inteiro (GB, minutos). Essa
leveza é o que torna prático subir dezenas de serviços na bancada e escalar centenas em produção (M20).

### Dockerfile: construir a sua imagem
Quando sua aplicação é própria (um job Python), você escreve um **Dockerfile** — a receita passo a
passo: parta de uma imagem base (`FROM python:3.12`), copie o código, instale dependências, defina o
comando. `docker build` transforma isso numa imagem reprodutível que roda igual em qualquer lugar (você
verá isso a fundo no M10).

### Portas e o `-p`: falar com o container
O container é isolado — para acessá-lo, você **mapeia uma porta** do host para uma do container com
`-p host:container`. Ex.: `-p 8888:8888` liga a porta 8888 da sua máquina à 8888 do Jupyter no
container. Por isso você abre `localhost:8888` e chega no serviço lá dentro.

### docker-compose: orquestrar vários serviços
Um pipeline real tem **vários** containers (banco + app + storage). Descrever cada `docker run` à mão é
inviável. O **`docker-compose.yml`** declara todos os serviços, portas, volumes e a rede entre eles num
arquivo versionado; `docker compose up` sobe **tudo** de uma vez, conectado. É exatamente a bancada do
curso — e um exemplo de **infraestrutura como código** (M13): o ambiente nasce de um arquivo, não de
cliques.

## 🔎 Exemplo
Você sobe a bancada com `docker compose up -d`. O Compose lê o `docker-compose.yml` e cria containers a
partir das **imagens** pinadas (`postgres:16.4`, `minio:...`), cada um na sua porta mapeada
(`5432:5432`, `9000:9000`). O Postgres guarda seus dados num **volume** (`pgdata`), então parar e subir
de novo **não perde** as tabelas. Tudo roda idêntico ao ambiente deste curso, no seu Windows, no Linux
do colega ou no CI — sem "na minha máquina funciona". Para derrubar, `docker compose down` (ou `down -v`
para apagar também os volumes).

## ⚠️ Erros comuns
- **Guardar dados sem volume** — o container é efêmero; ao recriá-lo, os dados somem.
- **Confundir imagem com container** — imagem é o molde imutável; container é a instância em execução.
- **Não pinar versões** (`postgres:latest`) — quebra a reprodutibilidade quando a `latest` muda.
- **Esquecer o `-p`** — o serviço roda, mas você não o alcança do host sem mapear a porta.
- **Embutir segredos na imagem** — use variáveis de ambiente/secrets, não hardcode (M14).

## 💼 O que o mercado espera
Entender imagem × container × volume, por que containers dão reprodutibilidade, mapear portas e subir um
ambiente com `docker-compose`. É esperado desde o júnior (a bancada de qualquer projeto de dados moderno
é conteinerizada) e é o pré-requisito para Kubernetes (M20).

:::{admonition} ✨ Em resumo
:class: resumo
- **Imagem** (molde imutável) → **container** (instância em execução, efêmero) → **volume** (dados persistentes).
- Containers **compartilham o kernel** do host: leves e rápidos (≠ VM), ótimos para subir muitos serviços.
- **`-p host:container`** mapeia a porta para você alcançar o serviço; **Dockerfile** constrói sua imagem.
- **docker-compose** sobe vários serviços conectados de um arquivo versionado — infraestrutura como código (M13).
:::

## 🧠 Quiz de recall
1. Qual a diferença entre imagem, container e volume?
   :::{dropdown} Resposta
   Imagem é o molde imutável e versionado; container é uma instância em execução dela (efêmera); volume é o armazenamento persistente que sobrevive ao container.
   :::
2. Por que um container é mais leve que uma máquina virtual?
   :::{dropdown} Resposta
   Porque compartilha o kernel do host e isola só a aplicação (MB, sobe em segundos), enquanto a VM emula um SO inteiro (GB, minutos).
   :::
3. Por que dados de um banco precisam de um volume?
   :::{dropdown} Resposta
   Porque o container é efêmero: ao ser recriado, o que estava só nele some. O volume persiste os dados fora do ciclo de vida do container.
   :::
4. O que faz `-p 8888:8888`?
   :::{dropdown} Resposta
   Mapeia a porta 8888 do host para a 8888 do container, permitindo acessar o serviço de dentro do container via localhost:8888.
   :::
5. Para que serve o docker-compose?
   :::{dropdown} Resposta
   Declarar e subir vários containers/serviços conectados (banco, app, storage) de um arquivo versionado com um comando — infraestrutura como código.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que usar Docker num projeto de dados?"
  :::{dropdown} Resposta modelo
  Para reprodutibilidade: empacoto a aplicação com todo o ambiente (runtime, libs, versões) numa imagem que roda igual na minha máquina, na do colega, no CI e em produção — acabando com o "na minha máquina funciona". Uso docker-compose para subir a stack inteira (banco, storage, orquestrador) de um arquivo versionado, o que também é infraestrutura como código e a base para escalar em Kubernetes.
  :::
- **P:** "Seu container de Postgres perdeu os dados ao reiniciar. O que houve?"
  :::{dropdown} Resposta modelo
  Faltou um volume. O container é efêmero: sem um volume mapeando o diretório de dados do Postgres para fora, ao recriar o container os dados somem. A correção é declarar um volume (ex.: `pgdata:/var/lib/postgresql/data`) no compose, para os dados persistirem entre reinícios.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Documentação oficial do Docker** — <https://docs.docker.com/get-started/> (imagens, containers, volumes).
- **Docker Compose** — <https://docs.docker.com/compose/> (orquestrar serviços).
- **Reis & Housley — Fundamentals of Data Engineering** (containers na infraestrutura de dados).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — containers e ambiente reprodutível. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — implantação e isolamento. <!-- @kleppmann2017 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
