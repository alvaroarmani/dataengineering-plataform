# O que é Engenharia de Dados

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Imagine uma empresa que quer responder "quanto vendemos por região no último trimestre?".
Os dados existem — mas espalhados: no sistema de vendas (um banco transacional), numa
planilha de metas, numa API de câmbio. Ninguém consegue responder rápido e com confiança,
porque **os dados não estão prontos para análise**. Deixá-los prontos, de forma confiável,
repetível e em escala, é o trabalho da **Engenharia de Dados**.

Repare no que a frase esconde: alguém precisa **extrair** os dados de cada fonte (sem
derrubar o sistema de vendas), **padronizar** formatos e moedas, **juntar** tudo,
**tratar** erros e duplicidades, **atualizar** isso todo dia sem intervenção manual, e
**garantir** que o número esteja certo. Cada um desses verbos é um problema de engenharia.

## O papel do engenheiro de dados

O engenheiro de dados é quem constrói e opera a **fundação** sobre a qual analistas,
cientistas de dados e produtos de IA trabalham. Uma forma clássica de enxergar isso é a
**"hierarquia de necessidades de dados"** (popularizada por Monica Rogati): antes de sonhar
com Machine Learning e IA no topo da pirâmide, é preciso ter a base — **coletar, mover,
armazenar e organizar** dados confiáveis. Sem essa base, o topo desaba.

```{mermaid}
flowchart TB
    IA["IA / ML / otimização"] --- AN["Analytics, métricas, A/B tests"]
    AN --- LIMPO["Dados limpos, transformados, agregados"]
    LIMPO --- MOVER["Mover / armazenar: pipelines, DW, lakes"]
    MOVER --- COLETAR["Coletar / instrumentar: gerar e ingerir dados"]
    style COLETAR fill:#1f8a4c,color:#fff
    style MOVER fill:#2fa564,color:#fff
```

O engenheiro de dados cuida da **base** da pirâmide (verde). Papéis vizinhos, para você
situar-se no mercado:

| Papel | Foco principal |
|---|---|
| **Engenheiro de Dados** | Pipelines, armazenamento, confiabilidade — deixa o dado *pronto e confiável*. |
| **Analytics Engineer** | Transformação/modelagem (dbt) na fronteira entre engenharia e analytics. |
| **Analista de Dados / BI** | Responde perguntas de negócio com os dados prontos. |
| **Cientista de Dados** | Modelos estatísticos/ML sobre os dados. |
| **Data / ML Platform Eng.** | Infra e ferramentas que os demais usam. |

:::{admonition} 📖 Da literatura — o que define a área hoje
:class: seealso
Reis & Housley definem Engenharia de Dados como o desenvolvimento, implementação e
manutenção de **sistemas e processos** que transformam dados brutos em informação de
alta qualidade e utilizável — e argumentam que a maturidade da nuvem deslocou o foco do
"como fazer caber/rodar" para **arquitetura, confiabilidade e valor de negócio**.
— *Fundamentals of Data Engineering*, cap. 1.
:::

:::{admonition} 🏭 Do mundo real — como o papel surgiu na indústria
:class: important
Maxime Beauchemin (criador do **Apache Airflow** e do **Apache Superset**, ex-Facebook e
Airbnb) descreve em *"The Rise of the Data Engineer"* como o papel emergiu quando times de
dados perceberam que **construir e operar a infraestrutura de dados** — pipelines, DW,
confiabilidade — era uma disciplina de engenharia por si só, distinta de análise e ciência
de dados. É leitura curta, aberta e essencial para entender de onde vem a profissão que você
está buscando. — Beauchemin (2017), freeCodeCamp.
:::

## O ciclo de vida do dado (e suas "correntes de fundo")

Um jeito útil de organizar a área é o **ciclo de vida da engenharia de dados**:

```{mermaid}
flowchart LR
    G[Geração<br/>apps, sensores, APIs] --> I[Ingestão]
    I --> A[Armazenamento]
    A --> T[Transformação]
    T --> S[Disponibilização<br/>analytics, BI, ML]
```

Mas as etapas visíveis são só metade da história. Atravessando **todas** elas há as
**correntes de fundo** (*undercurrents*) — as preocupações que separam um script que
"funcionou uma vez" de um sistema de produção:

- **Segurança** — quem acessa o quê; princípio do menor privilégio.
- **Gestão de dados (governança)** — catálogo, qualidade, propriedade, LGPD.
- **DataOps** — automação, CI/CD, monitoramento (cultura de operar dados como software).
- **Arquitetura de dados** — as decisões estruturais (onde os dados vivem, como fluem).
- **Orquestração** — coordenar e agendar tarefas com dependências (ex.: Airflow).
- **Engenharia de software** — código versionado, testado, legível.

:::{tip}
Guarde este mapa. Cada módulo do curso preenche uma peça: **ingestão** (M08),
**armazenamento/DW** (M06), **transformação** (M05, M07), **orquestração** (M09),
**qualidade** (M12), **governança** (M14), **software/DataOps** (M03, M13). O ciclo de
vida é o esqueleto que dá sentido ao resto.
:::

## OLTP vs OLAP: por que dois mundos

Dois tipos de carga de trabalho, otimizados de formas opostas:

- **OLTP** (*Online Transaction Processing*): sustenta a **operação**. Muitas transações
  pequenas e concorrentes (inserir um pedido, atualizar um saldo), baixa latência, forte
  consistência. Bancos como PostgreSQL/MySQL, geralmente **normalizados** e armazenados por
  **linha** (a linha inteira junta no disco — ótimo para ler/escrever "um pedido").
- **OLAP** (*Online Analytical Processing*): serve à **análise**. Poucas consultas, porém
  **grandes**, que varrem milhões de linhas e **agregam** poucas colunas (soma de vendas
  por mês). Sistemas como BigQuery/Redshift/Snowflake, geralmente **desnormalizados** e
  armazenados por **coluna**.

### Por que armazenamento colunar acelera análise

Imagine uma tabela de 50 colunas e 100 milhões de linhas. A pergunta é "receita total por
mês" — usa só 2 colunas (`valor`, `data`).

- **Por linha:** para somar `valor`, o sistema precisa ler *todas as 50 colunas* de cada
  linha (elas estão intercaladas no disco). Desperdício enorme de I/O.
- **Por coluna:** os valores de `valor` estão **contíguos** no disco. Lê-se só as 2 colunas
  necessárias, ignorando as outras 48. Além disso, dados do mesmo tipo lado a lado
  **comprimem muito melhor** (ex.: muitos valores repetidos → *run-length encoding*).

Resultado: consultas analíticas ficam ordens de magnitude mais rápidas e baratas. É por
isso que Data Warehouses modernos são **colunares**.

:::{admonition} 📖 Da literatura — armazenamento orientado a coluna
:class: seealso
Kleppmann mostra que, em cargas analíticas que tocam poucas colunas de tabelas enormes, o
**armazenamento colunar** reduz drasticamente o volume lido do disco e habilita compressão
agressiva — a base técnica dos data warehouses.
— *Designing Data-Intensive Applications*, cap. 3 ("Transaction Processing or Analytics?").
:::

## Batch vs streaming: o espectro da latência

- **Batch** (lote): processa dados **limitados** (*bounded*) em intervalos — ex.: todo dia
  às 3h, ou de hora em hora. Simples, barato, fácil de reprocessar. **É a maioria dos casos.**
- **Streaming** (fluxo): processa dados **ilimitados** (*unbounded*), evento a evento, em
  tempo (quase) real. Poderoso quando a latência importa (fraude, monitoramento, dashboards
  ao vivo), porém mais complexo (ordem, duplicidade, estado, janelas de tempo).

Não é preto-no-branco: existe um **espectro** — do batch diário ao *micro-batch* (a cada
poucos minutos) ao streaming contínuo. Duas arquiteturas históricas para combiná-los:

- **Lambda:** mantém uma camada batch (precisa, lenta) e uma camada de velocidade (rápida,
  aproximada) em paralelo — poderoso, mas custoso de manter (lógica duplicada).
- **Kappa:** trata **tudo como stream**, reprocessando o histórico a partir de um log de
  eventos — simplifica ao custo de exigir infra de streaming robusta.

:::{warning}
**Erro clássico de iniciante:** adotar streaming "porque é moderno". Streaming multiplica a
complexidade operacional. Regra prática: **comece por batch**; só vá para streaming quando
houver um requisito real de baixa latência que o negócio pague para ter.
:::

## Formatos de arquivo importam (CSV vs Parquet)

Um detalhe que separa iniciante de profissional:

| | CSV | Parquet |
|---|---|---|
| Layout | Linha, texto | **Coluna, binário** |
| Schema/tipos | Não guarda (tudo é string) | **Guarda** (tipos, nulos) |
| Compressão | Ruim | **Ótima** (por coluna) |
| Leitura seletiva de colunas | Não | **Sim** (lê só o necessário) |
| Uso | Troca rápida, humanos | **Analytics em escala** |

Por isso, em pipelines sérios, dados brutos costumam pousar como **Parquet** (colunar) e
não CSV. Você usará ambos no curso e sentirá a diferença de desempenho no M03/M11.

## DW, Data Lake e Lakehouse (e a virada ETL → ELT)

Uma linha do tempo ajuda a entender *por que* existem três coisas:

1. **Data Warehouse (anos 1990):** repositório **estruturado e modelado** para análise
   (Inmon, Kimball). Dados limpos, schema definido — ótimo para BI. Caro e rígido para
   dados brutos/variados.
2. **Data Lake (era Hadoop, ~2010):** guarda **dados brutos** em qualquer formato, barato,
   em *object storage* (S3/GCS/MinIO). Flexível — mas, sem governança, vira um **"data
   swamp"** (pântano): dados que ninguém confia nem acha.
3. **Lakehouse (atual):** junta os dois — a flexibilidade/custo do lake com
   **transações ACID, schema e time travel** via formatos de tabela como **Delta Lake** e
   **Apache Iceberg**. É a arquitetura em ascensão.

Essa evolução andou junto com a mudança de **ETL → ELT**:

- **ETL** (*Extract, Transform, Load*): transforma **antes** de carregar. Comum quando
  computação/armazenamento eram caros — só entrava no DW o dado já refinado.
- **ELT** (*Extract, Load, Transform*): carrega o **bruto** primeiro, transforma **depois**,
  já dentro do DW/lakehouse. Habilitado pela nuvem barata e por DWs colunares poderosos — é
  o padrão do **Modern Data Stack** (e do dbt, que você verá no M07).

## Padrões de arquitetura que você vai ouvir

- **Modern Data Stack:** ingestão gerenciada → DW cloud (BigQuery/Snowflake) → dbt → BI. Foco em ELT e ferramentas gerenciadas.
- **Arquitetura Medalhão (bronze/silver/gold):** camadas de refinamento — *bronze* (bruto),
  *silver* (limpo/conformado), *gold* (modelado para consumo). Você usará isso no TCC.
- **Data Mesh:** abordagem **organizacional** — descentraliza a responsabilidade pelos dados
  para os **domínios** de negócio, tratando "dados como produto". Menos uma tecnologia, mais
  um modelo de governança para empresas grandes.

## Um conceito que atravessa tudo: idempotência

Guarde esta palavra desde já. Uma operação é **idempotente** quando executá-la várias vezes
produz o **mesmo resultado** que executá-la uma vez. Em dados, isso é vital: pipelines
falham e são **reprocessados** — se rodar de novo o dia 10 **duplicar** as vendas do dia 10,
seu pipeline está quebrado. Projetar para idempotência (ex.: "sobrescrever a partição do
dia" em vez de "inserir") é marca de maturidade — tema recorrente do M08/M09.

## 🔎 Exemplo integrador

Voltando ao caso de "vendas por região": **ingerimos** pedidos do OLTP e câmbio da API
(landing em Parquet no lake), **transformamos** em camadas bronze→silver→gold modelando um
star schema, **disponibilizamos** ao BI — tudo **orquestrado** para rodar diariamente de
forma **idempotente**, com **testes de qualidade** e **governança**. Todo o curso constrói,
peça por peça, exatamente essa máquina — até o TCC.

## ⚠️ Erros comuns
- Pensar que "engenharia de dados = pandas". A área é sobre **sistemas e confiabilidade**.
- Rodar análise pesada direto no banco de produção (OLTP) — impacta a operação.
- Tratar **data lake** e **data warehouse** como sinônimos.
- Adotar **streaming** sem necessidade real de baixa latência.
- Salvar tudo como **CSV** onde Parquet economizaria tempo e dinheiro.
- Escrever pipelines **não idempotentes** (reprocessar duplica dados).

## 💼 O que o mercado espera
Que você tenha o **mapa mental** e o **vocabulário**: posicionar DW/lake/lakehouse,
batch/stream, OLTP/OLAP, ETL/ELT, e justificar escolhas. Perguntas conceituais assim são
rotina em entrevistas Jr — e a base para tudo o que vem depois.

:::{admonition} ✨ Em resumo
:class: resumo
- **Engenharia de dados** = construir e operar os sistemas que deixam o dado *pronto e confiável*.
- **OLTP** (operação, por linha) ≠ **OLAP** (análise, por coluna) — o colunar é o que acelera a análise.
- **DW / Lake / Lakehouse** e **batch / streaming**: escolha pelo problema, não pela moda.
- **Idempotência** é chave: reprocessar não pode duplicar.
:::

## 🧠 Quiz de recall
Responda de memória, depois confira:

1. Qual a diferença entre OLTP e OLAP, e por que separá-los?
   :::{dropdown} Resposta
   OLTP sustenta a operação (muitas escritas pequenas, orientado a linha, normalizado);
   OLAP serve à análise (leituras grandes e agregações, orientado a coluna, desnormalizado).
   Separamos para não degradar a operação e para otimizar cada carga de trabalho.
   :::
2. Por que o armazenamento colunar acelera consultas analíticas?
   :::{dropdown} Resposta
   Consultas analíticas tocam poucas colunas de tabelas enormes; no formato colunar essas
   colunas ficam contíguas, então lê-se só o necessário (menos I/O) e comprime-se muito
   melhor (dados do mesmo tipo juntos).
   :::
3. Cite três "correntes de fundo" (undercurrents) do ciclo de vida do dado.
   :::{dropdown} Resposta
   Quaisquer três entre: segurança, gestão/governança de dados, DataOps, arquitetura de
   dados, orquestração, engenharia de software.
   :::
4. O que mudou de ETL para ELT e por quê?
   :::{dropdown} Resposta
   Em ELT carrega-se o dado bruto primeiro e transforma-se depois, já dentro do DW/lakehouse.
   A mudança foi habilitada por armazenamento/compute de nuvem baratos e DWs colunares
   potentes — é o padrão do Modern Data Stack (e do dbt).
   :::
5. O que é idempotência e por que importa em pipelines?
   :::{dropdown} Resposta
   Uma operação é idempotente quando executá-la N vezes dá o mesmo resultado que uma vez.
   Importa porque pipelines falham e são reprocessados; sem idempotência, reprocessar duplica
   ou corrompe dados.
   :::
6. Quando um Data Lake vira um "data swamp"?
   :::{dropdown} Resposta
   Quando se acumulam dados brutos sem governança (catálogo, qualidade, propriedade): ninguém
   sabe o que existe nem confia no conteúdo. O Lakehouse surge para dar schema/ACID a essa base.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Explique o ciclo de vida do dado."
  :::{dropdown} Resposta modelo
  Geração → Ingestão → Armazenamento → Transformação → Disponibilização, com as correntes de
  fundo (segurança, governança, DataOps, arquitetura, orquestração, engenharia de software)
  permeando todas as etapas.
  :::
- **P:** "Data lake e data warehouse são a mesma coisa?"
  :::{dropdown} Resposta modelo
  Não. O warehouse é estruturado e modelado para análise/BI; o lake guarda dados brutos em
  qualquer formato, barato e flexível. O lakehouse combina os dois com transações ACID e schema.
  :::
- **P:** "Quando você escolheria streaming em vez de batch?"
  :::{dropdown} Resposta modelo
  Só quando há requisito real de baixa latência (ex.: detecção de fraude, monitoramento ao
  vivo) que justifique a complexidade extra. Na dúvida, batch — mais simples, barato e fácil
  de reprocessar.
  :::
- **P:** "Por que Parquet em vez de CSV num data lake?"
  :::{dropdown} Resposta modelo
  Parquet é colunar e binário: guarda schema/tipos, comprime muito melhor e permite ler só as
  colunas necessárias — mais rápido e barato em analytics. CSV não guarda tipos e é ineficiente em escala.
  :::
- **P:** "O que é Data Mesh?"
  :::{dropdown} Resposta modelo
  Uma abordagem organizacional que descentraliza a responsabilidade pelos dados para os
  domínios de negócio, tratando dados como produto. É mais governança/organização do que uma
  tecnologia específica, voltada a empresas grandes.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley**, *Fundamentals of Data Engineering* — cap. 1 (o que é a área) e cap. 2 (ciclo de vida + undercurrents). *Ponto de partida essencial.*
- **Kleppmann**, *Designing Data-Intensive Applications* — cap. 1 (confiabilidade/escalabilidade/manutenibilidade) e cap. 3 (row vs column stores).
- **Kimball & Ross**, *The Data Warehouse Toolkit* — introdução (por que modelar para análise) — aprofundado no M05.
- **Dehghani**, *Data Mesh Principles* (martinfowler.com) — para o conceito de Data Mesh.

Mais materiais e vídeos em [recursos.md](recursos.md).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (O'Reilly, 2022) — cap. 1–2. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (O'Reilly, 2017) — cap. 1 e 3. <!-- @kleppmann2017 -->
- Rogati, M. *The AI Hierarchy of Needs* (2017) — [artigo aberto](https://hackernoon.com/the-ai-hierarchy-of-needs-18f111fcc007). <!-- @rogati2017 -->
- Beauchemin, M. *The Rise of the Data Engineer* (2017) — [artigo aberto](https://www.freecodecamp.org/news/the-rise-of-the-data-engineer-91be18f1e603/). <!-- @beauchemin2017 -->
- Dehghani, Z. *Data Mesh Principles and Logical Architecture* (martinfowler.com, 2020) — [artigo aberto](https://martinfowler.com/articles/data-mesh-principles.html). <!-- @dehghani2020 -->

*Acessado em: 2026-08-20.*

---
**Revisado em:** 2026-08-20
