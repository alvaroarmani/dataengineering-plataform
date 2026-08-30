# Redes, volumes e Compose multi-serviço

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Um pipeline de dados não é **um** container — são vários que **conversam** (app → Postgres →
MinIO) e que precisam **guardar dados** entre reinícios. Se cada um subir isolado e sem
persistência, nada funciona junto e você perde os dados no `down`. **Redes** (para eles se
acharem), **volumes** (para persistir) e **Compose** (para subir tudo junto) resolvem isso — é
exatamente como a bancada do curso funciona.

## 💡 Conceito (o porquê)

### Redes: containers se acham pelo nome
Containers na **mesma rede** se comunicam usando o **nome do serviço** como host. No Compose,
todos os serviços entram numa rede padrão — por isso a app conecta em `postgres:5432` (não
`localhost`). `localhost` **dentro** de um container é ele mesmo, não o host nem os vizinhos.

### Volumes: dados que sobrevivem
O sistema de arquivos de um container é **efêmero** — some quando ele é recriado. Para
**persistir** (o banco não pode perder os dados), usa-se **volumes**:
- **Named volume:** gerenciado pelo Docker (`pgdata:/var/lib/postgresql/data`) — persistência de dados.
- **Bind mount:** mapeia uma pasta do host (`./dags:/opt/airflow/dags`) — ótimo para
  desenvolvimento (edita no host, reflete no container).

### Portas: host ↔ container
`ports: ["8080:80"]` publica a porta **80 do container** na porta **8080 do host** (formato
`host:container`). É assim que você abre `http://localhost:8080` no navegador para um serviço
que escuta na 80 lá dentro. Sem publicar a porta, o serviço só é acessível **dentro da rede**.

### Compose: o stack inteiro num arquivo
`docker-compose.yml` declara **vários serviços**, suas imagens, portas, volumes, redes,
variáveis e **dependências** (`depends_on`) — e sobe tudo com `docker compose up`. É
infraestrutura como código, reprodutível. `depends_on` define **ordem de início** (o Docker
sobe o Postgres antes do que depende dele); com **healthcheck**, espera ficar saudável.

```{mermaid}
flowchart LR
    A[app] -->|postgres:5432| P[(postgres<br/>vol: pgdata)]
    A -->|minio:9000| M[(minio<br/>vol: miniodata)]
    subgraph rede default
      A
      P
      M
    end
```

## 🔎 Exemplo
A bancada (`ambiente/docker-compose.yml`): `jupyter`, `postgres` (com volume `pgdata`), `minio`
(volume `miniodata`) na mesma rede. O Jupyter conecta em `postgres:5432` pelo **nome**; o
Postgres persiste em `pgdata` (um `down`/`up` não perde os dados); a porta `5432:5432` expõe o
banco ao host para você conectar do seu editor.

:::{admonition} 📖 Da literatura
:class: seealso
A documentação do Compose descreve serviços numa **rede compartilhada** (resolvidos por nome),
**volumes** para persistência e **`depends_on`/healthcheck** para ordem de inicialização — o
modelo para orquestrar múltiplos containers localmente de forma reprodutível. — Docker Compose,
documentação oficial.
:::

:::{admonition} 🏭 Do mundo real
:class: important
"Funciona na minha máquina" morre com Compose: o stack inteiro (app + bancos + filas) sobe
igual em qualquer lugar, com dados persistidos em volumes e serviços se achando por nome. É a
base de ambientes de dev e de muitos deploys locais/staging. — Docker, docs oficiais.
:::

## ⚠️ Erros comuns
- Conectar em **`localhost`** entre containers — dentro do container, `localhost` é ele mesmo; use o **nome do serviço**.
- **Sem volume** no banco — os dados somem ao recriar o container.
- Confundir a ordem de **`ports`** (`host:container`) — publica na porta errada.
- Achar que **`depends_on`** espera o serviço ficar *pronto* — ele só espera **iniciar**; use **healthcheck** para prontidão.
- Bind mount cobrindo uma pasta que a imagem precisa — pode "esconder" arquivos do container.

## 💼 O que o mercado espera
Subir um pipeline multi-serviço com Compose (rede, volumes, depends_on) é o "monte o ambiente"
de muitas vagas e do seu TCC. Entender rede/volume/porta evita as dores mais comuns de quem
começa com containers.

:::{admonition} ✨ Em resumo
:class: resumo
- **Rede:** containers se acham pelo **nome do serviço** (não `localhost`); Compose cria uma rede padrão.
- **Volumes:** persistem dados (named volume) ou mapeiam pastas do host (bind mount) — sem eles, dados somem.
- **Portas** `host:container` publicam o serviço no host; sem publicar, só é acessível na rede.
- **Compose** declara o stack inteiro (serviços, volumes, redes, `depends_on`/healthcheck) e sobe tudo junto.
:::

## 🧠 Quiz de recall
1. Como um container acha outro no Compose?
   :::{dropdown} Resposta
   Pelo nome do serviço como host (ex.: postgres:5432), pois estão na mesma rede. localhost dentro do container é ele mesmo.
   :::
2. Por que um banco precisa de volume?
   :::{dropdown} Resposta
   O filesystem do container é efêmero (some ao recriar); o volume persiste os dados entre reinícios/recriações.
   :::
3. O que significa `ports: ["8080:80"]`?
   :::{dropdown} Resposta
   Publica a porta 80 do container na 8080 do host (host:container) — você acessa via localhost:8080.
   :::
4. `depends_on` garante que o serviço está pronto?
   :::{dropdown} Resposta
   Não — só garante a ordem de início. Para esperar prontidão, use um healthcheck (condition: service_healthy).
   :::
5. Named volume vs bind mount?
   :::{dropdown} Resposta
   Named volume é gerenciado pelo Docker (persistência de dados); bind mount mapeia uma pasta do host (bom para dev, edita no host e reflete no container).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Sua app não conecta no Postgres do Compose. O que checa?"
  :::{dropdown} Resposta modelo
  Primeiro o host: dentro do container tem que ser o nome do serviço (`postgres`), não `localhost`. Depois, se estão na mesma rede, se a porta/credenciais batem, e se uso healthcheck + depends_on para a app só subir quando o banco estiver pronto.
  :::
- **P:** "Ao dar down/up, os dados do banco somem. Por quê?"
  :::{dropdown} Resposta modelo
  Falta volume. O filesystem do container é efêmero; preciso de um named volume mapeado no diretório de dados do Postgres para persistir entre recriações.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Docker Compose docs** — *Services*, *Networking*, *Volumes*, *depends_on / healthcheck*.

## 📚 Referências
- Docker — Documentação oficial (Compose: rede, volumes, depends_on, healthcheck). <!-- @docs-docker -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — ambientes reprodutíveis. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
