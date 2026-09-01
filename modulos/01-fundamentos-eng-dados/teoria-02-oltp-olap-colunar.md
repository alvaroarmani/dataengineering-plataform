# OLTP vs OLAP e o armazenamento colunar

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Uma pergunta aparentemente boba tem uma resposta que organiza boa parte da engenharia de dados:
por que a empresa não usa **um banco só** para tudo? Por que o sistema que processa a sua compra
(rápido, uma linha por vez) é diferente do sistema que gera o relatório de vendas do trimestre (que
varre milhões de linhas)? A resposta está na distinção **OLTP × OLAP** e na forma como os dados são
**fisicamente armazenados** — por linha ou por coluna. Entender isso explica por que existem bancos
transacionais **e** data warehouses, por que o Parquet (M06) é colunar, e por que uma consulta
analítica no banco errado custa caro e trava. É um dos fundamentos que mais aparece em entrevista.

## 💡 Conceito (o porquê)

### Dois perfis de carga
- **OLTP (Online Transaction Processing):** o sistema **operacional** que roda o negócio em tempo
  real — registra pedidos, pagamentos, cadastros. Faz **muitas operações pequenas** (inserir/atualizar
  uma linha), precisa de baixa latência e **consistência** (ACID). Ex.: o Postgres por trás de um app.
- **OLAP (Online Analytical Processing):** o sistema **analítico** que responde perguntas sobre o
  histórico — "receita por região no ano". Faz **poucas consultas grandes** que varrem e agregam
  milhões de linhas, lendo **poucas colunas** de cada vez. Ex.: BigQuery, um data warehouse.

Misturar os dois no mesmo banco é o erro clássico: rodar um relatório pesado no banco de produção
degrada o app; modelar o analítico como transacional torna as consultas lentas.

### Por que o armazenamento físico muda tudo
A diferença profunda está em **como as linhas ficam no disco**:
- **Armazenamento por linha (row-oriented):** os valores de uma **linha** ficam juntos. Ler ou gravar
  **um registro inteiro** é rápido — ótimo para OLTP ("me dê o pedido 42").
- **Armazenamento colunar (column-oriented):** os valores de uma **coluna** ficam juntos. Uma consulta
  analítica que só precisa de 3 colunas de 100 lê **só essas 3** — em vez de arrastar as 100. Menos
  I/O, menos custo. É por isso que warehouses e o Parquet são colunares.

Repare: a mesma pergunta ("some o `valor` de 10 milhões de linhas") lê **1 coluna** no colunar e
**as 100** no formato por linha. Daí a diferença de desempenho (e de custo na nuvem, M21) ser enorme.

### Colunar também comprime melhor
Como uma coluna guarda valores do **mesmo tipo e domínio** (todos os estados, todos os preços), eles
se repetem e comprimem muito bem (dictionary/run-length encoding). Menos bytes no disco = menos I/O =
mais rápido e barato. Compressão é quase de graça no colunar e difícil no formato por linha.

### A consequência arquitetural
Por isso a empresa mantém **os dois mundos**: bancos OLTP (por linha) rodam a operação; os dados são
**copiados** (por ingestão, M08) para um sistema OLAP (colunar) onde a análise acontece sem atrapalhar
a produção. Essa separação é o motivo de existir a engenharia de dados: mover e transformar dados do
mundo transacional para o analítico.

## 🔎 Exemplo
No app de e-commerce, cada compra grava uma linha no Postgres **OLTP** (rápido, por linha,
consistente). Toda noite, um pipeline copia esses dados para o **BigQuery** (OLAP, colunar). O analista
roda "receita por categoria por mês" — uma consulta que varre milhões de linhas mas lê só 3 colunas
(`data`, `categoria`, `valor`). No colunar, ela lê **só essas 3 colunas comprimidas** e responde em
segundos, sem tocar no banco de produção. A mesma consulta no Postgres transacional arrastaria todas as
colunas de todas as linhas e ainda concorreria com as compras dos clientes.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann dedica o capítulo de armazenamento à distinção **row-oriented vs column-oriented**, mostrando
por que o colunar domina o processamento analítico (leitura seletiva de colunas + compressão). Reis &
Housley tratam OLTP e OLAP como os dois polos que o ciclo de vida do dado conecta. — *Designing
Data-Intensive Applications* (cap. 3); *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
"Não rode analytics no banco de produção" é uma das primeiras lições operacionais de dados: uma
consulta analítica pesada num OLTP degrada o app inteiro. A solução — copiar para um sistema colunar —
é literalmente a razão de existir data warehouses e formatos como Parquet. — Kleppmann; Reis & Housley.
:::

## ⚠️ Erros comuns
- **Rodar relatórios no banco de produção (OLTP)** — degrada o app e é lento.
- **Modelar o analítico como transacional** (muito normalizado) — consultas lentas, sem tirar proveito do colunar.
- **Achar que colunar é "sempre melhor"** — para gravar/ler uma linha inteira (OLTP), o formato por linha vence.
- **Ignorar a compressão** — parte enorme do ganho colunar vem de comprimir colunas homogêneas.
- **Confundir OLTP com OLAP** na entrevista — é a distinção conceitual mais cobrada.

## 💼 O que o mercado espera
Distinguir OLTP de OLAP com exemplos, explicar row vs colunar e **por que** o colunar acelera analytics
(leitura seletiva + compressão), e entender que os dois mundos coexistem ligados por ingestão. "Quando
usar um banco transacional vs um data warehouse?" é pergunta quase garantida.

:::{admonition} ✨ Em resumo
:class: resumo
- **OLTP** = operacional (muitas operações pequenas, por linha, ACID); **OLAP** = analítico (poucas consultas grandes, colunar).
- **Colunar** guarda cada coluna junta → a consulta lê **só as colunas necessárias** (menos I/O e custo) e **comprime** melhor.
- Formato **por linha** vence para ler/gravar registros inteiros (OLTP); **colunar** vence para agregações (OLAP).
- Os dois mundos **coexistem**: dados vão do OLTP para o OLAP por ingestão — a razão de existir a eng. de dados.
:::

## 🧠 Quiz de recall
1. Qual a diferença essencial entre OLTP e OLAP?
   :::{dropdown} Resposta
   OLTP é operacional: muitas operações pequenas (inserir/atualizar uma linha), baixa latência, ACID. OLAP é analítico: poucas consultas grandes que varrem e agregam milhões de linhas, lendo poucas colunas.
   :::
2. Por que o armazenamento colunar acelera consultas analíticas?
   :::{dropdown} Resposta
   Porque guarda cada coluna junta: a consulta lê só as colunas necessárias (em vez de todas), reduzindo drasticamente o I/O — e colunas homogêneas comprimem muito bem.
   :::
3. Quando o formato por linha é melhor que o colunar?
   :::{dropdown} Resposta
   Quando você lê ou grava um registro inteiro por vez (OLTP): os valores da linha ficam juntos, então a operação é rápida.
   :::
4. Por que não se deve rodar relatórios no banco de produção?
   :::{dropdown} Resposta
   Porque uma consulta analítica pesada varre muitos dados e concorre com as transações do app, degradando a latência da produção; o certo é copiar para um sistema OLAP.
   :::
5. Por que colunar comprime melhor?
   :::{dropdown} Resposta
   Porque cada coluna guarda valores do mesmo tipo e domínio, que se repetem — permitindo compressão eficiente (dictionary/run-length), reduzindo bytes e I/O.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Quando você usaria um banco transacional e quando um data warehouse?"
  :::{dropdown} Resposta modelo
  Banco transacional (OLTP) para a operação em tempo real do app — muitas escritas/leituras pequenas, consistência ACID, armazenamento por linha. Data warehouse (OLAP) para análise sobre o histórico — consultas grandes que agregam milhões de linhas lendo poucas colunas, armazenamento colunar. Os dados vão do OLTP para o OLAP por ingestão; nunca rodo analytics pesado no banco de produção.
  :::
- **P:** "Por que o Parquet é mais rápido que o CSV para análise?"
  :::{dropdown} Resposta modelo
  Porque o Parquet é colunar e comprimido: uma consulta que precisa de 3 colunas lê só essas 3 (o CSV, por linha, teria que ler tudo), e as colunas homogêneas comprimem bem, reduzindo I/O. Para agregações analíticas isso é ordens de grandeza mais rápido — e mais barato na nuvem, onde se paga por bytes lidos.
  :::
- **P:** "O relatório noturno está deixando o app lento. O que houve e como resolver?"
  :::{dropdown} Resposta modelo
  Provavelmente o relatório roda direto no banco OLTP de produção, concorrendo com as transações. A correção é separar os mundos: copiar os dados para um sistema OLAP colunar (data warehouse) por um pipeline de ingestão e rodar o analytics lá, tirando a carga pesada da produção.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 3, row vs column storage).
- **Reis & Housley — Fundamentals of Data Engineering** (OLTP/OLAP no ciclo de vida).
- **Documentação do Apache Parquet** — formato colunar na prática.

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — armazenamento row vs colunar. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — OLTP e OLAP. <!-- @reis2022 -->
- Armbrust, M. et al. *Lakehouse: A New Generation of Open Platforms* (2021) — armazenamento colunar. <!-- @armbrust2020 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
