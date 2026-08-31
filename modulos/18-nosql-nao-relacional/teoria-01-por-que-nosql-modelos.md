# Por que NoSQL? Modelos de dados não-relacionais e trade-offs

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você aprendeu SQL e o modelo relacional (M04) — e ele é excelente: consistente, com esquema rígido,
transações ACID e JOINs poderosos. Mas nem todo problema cabe numa tabela. Como guardar o **carrinho
de sessão** de milhões de usuários com latência de 1ms? Como aceitar **milhões de escritas por
segundo** de sensores, distribuídas por vários data centers, sem um único servidor virar gargalo?
Como armazenar documentos com **estruturas variáveis** (cada produto com atributos diferentes) sem
alterar o esquema toda semana? Para essas cargas, o modelo relacional trava — e é aí que entram os
bancos **NoSQL** ("not only SQL"): famílias de bancos com modelos de dados e trade-offs diferentes,
projetados para **escala horizontal, flexibilidade de esquema e padrões de acesso específicos**.

## 💡 Conceito (o porquê)

### NoSQL não é "melhor que SQL" — é diferente
NoSQL não substitui o relacional; **complementa**. Cada família troca algumas garantias do modelo
relacional (esquema rígido, JOINs, ACID forte) por outras vantagens (escala, flexibilidade,
velocidade em um padrão de acesso). A pergunta certa nunca é "SQL ou NoSQL?", e sim **"qual modelo
serve a este padrão de acesso e a esta escala?"**.

### As quatro famílias
- **Documento** (MongoDB): guarda **documentos** (JSON/BSON) com estrutura flexível. Cada registro
  carrega seus dados aninhados — ótimo para catálogos, perfis, conteúdo com formato variável.
- **Key-value** (Redis): um dicionário gigante e rapidíssimo — você guarda e busca por **chave**.
  Ideal para cache, sessões, contadores. Simples e de latência mínima.
- **Wide-column / colunar-distribuído** (Cassandra): tabelas particionadas por chave, otimizadas
  para **escrita massiva** e escala horizontal em muitos nós. Modela-se **pela consulta**.
- **Grafo** (Neo4j): nós e arestas, para dados **altamente conectados** (redes sociais, fraude,
  recomendação) — consultas de relacionamento que seriam JOINs recursivos caros no relacional.

(Um quinto uso comum, **time-series**, é tratado na unidade 3: métricas/eventos indexados por tempo.)

### Schema-on-write vs schema-on-read
- O relacional é **schema-on-write**: você define o esquema antes; o banco recusa dados fora dele.
  Garante consistência estrutural, ao custo de rigidez.
- Muitos NoSQL são **schema-on-read**: gravam quase qualquer coisa; a estrutura é interpretada na
  leitura pela aplicação. Dá flexibilidade (formatos que evoluem), ao custo de a aplicação ter de
  lidar com variações. Nenhum é "certo" — depende de quanto a estrutura muda.

### O trade-off central: consistência × disponibilidade (CAP)
Sistemas distribuídos enfrentam o **teorema CAP**: sob uma **partição de rede** (P — nós que não se
falam, algo inevitável em escala), você precisa escolher entre **consistência** (C — todos veem o
mesmo dado) e **disponibilidade** (A — o sistema responde mesmo assim). Muitos NoSQL priorizam **A**
e oferecem **consistência eventual**: as réplicas convergem "em algum momento", aceitando ler um
dado ligeiramente desatualizado em troca de sempre responder e escalar. O relacional clássico tende a
priorizar **C**. Escolher a família NoSQL é, em boa parte, escolher onde você fica nesse trade-off.

### Desnormalização: o modelo segue a consulta
No relacional você **normaliza** (evita repetição) e junta com JOINs na hora da leitura. Em muitos
NoSQL não há JOIN eficiente distribuído — então você **desnormaliza**: duplica dados e modela **pela
consulta que vai rodar**, gravando já no formato que a leitura precisa. Troca-se espaço e escrita
duplicada por leitura rápida e escalável.

## 🔎 Exemplo
Um e-commerce usa **vários** bancos (persistência poliglota): Postgres para pedidos e pagamentos
(precisa de ACID); **MongoDB** para o catálogo de produtos (cada categoria com atributos diferentes —
esquema flexível); **Redis** para o carrinho de sessão e cache de páginas (latência mínima);
**Cassandra** para o histórico de eventos de navegação (escrita massiva, escala horizontal). Cada
carga no banco que melhor a serve — nenhum banco único faria tudo bem.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann compara os **modelos de dados** (relacional, documento, grafo) e dedica capítulos a
**replicação**, **particionamento** e **consistência**, explicando os trade-offs (incluindo CAP e
consistência eventual) que definem os bancos NoSQL. Reis & Housley tratam os sistemas de
armazenamento NoSQL como parte do ciclo de vida do dado. — *Designing Data-Intensive Applications*
(caps. 2, 5, 6, 9); *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Empresas grandes praticam **persistência poliglota**: não existe "o banco da empresa", e sim o banco
certo por carga. Netflix usa Cassandra para escala de escrita; muitos sistemas usam Redis para cache
na frente do banco principal. Saber **escolher a família** pelo padrão de acesso é uma competência de
engenharia de dados tão importante quanto saber SQL. — prática de mercado; Kleppmann.
:::

## ⚠️ Erros comuns
- **"NoSQL é sempre mais escalável/melhor"** — é um trade-off; o relacional continua ótimo para muita coisa.
- **Modelar NoSQL como no relacional** — normalizar e esperar JOINs; o certo é modelar pela consulta e desnormalizar.
- **Ignorar consistência eventual** — assumir leitura sempre atualizada onde o banco prioriza disponibilidade.
- **Usar um só banco para tudo** — perder a vantagem da persistência poliglota.
- **Escolher a família pela moda**, não pelo padrão de acesso e escala.

## 💼 O que o mercado espera
Conhecer as quatro famílias e seus casos, entender schema-on-read, CAP/consistência eventual e
desnormalização — e saber **escolher** a família pelo padrão de acesso. "Quando você usaria NoSQL em
vez de um relacional?" é pergunta clássica.

:::{admonition} ✨ Em resumo
:class: resumo
- **NoSQL complementa o SQL**: cada família troca garantias (esquema/JOIN/ACID) por escala, flexibilidade ou velocidade.
- Famílias: **documento** (Mongo), **key-value** (Redis), **wide-column** (Cassandra), **grafo** (Neo4j) — + time-series.
- **Schema-on-read** dá flexibilidade; **CAP/consistência eventual** troca C por A e escala.
- Modela-se **pela consulta** (desnormalização), não normalizando como no relacional.
:::

## 🧠 Quiz de recall
1. NoSQL substitui o relacional? Por quê?
   :::{dropdown} Resposta
   Não; complementa. Cada família troca garantias do relacional por vantagens específicas (escala, flexibilidade, velocidade). A escolha é pelo padrão de acesso e escala, não "um ou outro".
   :::
2. Cite as quatro famílias NoSQL e um caso de cada.
   :::{dropdown} Resposta
   Documento (catálogo/perfil), key-value (cache/sessão), wide-column (escrita massiva/eventos), grafo (dados conectados: rede social/fraude).
   :::
3. Qual a diferença entre schema-on-write e schema-on-read?
   :::{dropdown} Resposta
   Schema-on-write (relacional) exige o esquema antes e recusa dados fora dele; schema-on-read (muitos NoSQL) grava estruturas flexíveis e a aplicação interpreta na leitura.
   :::
4. O que o teorema CAP diz, e o que muitos NoSQL escolhem?
   :::{dropdown} Resposta
   Sob partição de rede (P), escolhe-se entre consistência (C) e disponibilidade (A). Muitos NoSQL priorizam A com consistência eventual (réplicas convergem depois).
   :::
5. Por que se desnormaliza em NoSQL?
   :::{dropdown} Resposta
   Porque não há JOIN eficiente distribuído; modela-se pela consulta e duplica-se o dado para ler rápido e escalar, ao custo de espaço e escrita duplicada.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Quando você usaria NoSQL em vez de um banco relacional?"
  :::{dropdown} Resposta modelo
  Quando o padrão de acesso ou a escala não cabem bem no relacional: esquema muito variável (documento), latência mínima de cache/sessão (key-value), escrita massiva distribuída (wide-column) ou dados altamente conectados (grafo). Se preciso de ACID forte e JOINs complexos, fico no relacional. Na prática uso persistência poliglota: o banco certo por carga.
  :::
- **P:** "O que é consistência eventual e qual o risco?"
  :::{dropdown} Resposta modelo
  As réplicas convergem para o mesmo valor "em algum momento", não instantaneamente — em troca, o sistema fica disponível e escala (lado A do CAP). O risco é ler um dado ligeiramente desatualizado logo após uma escrita. Aceito isso onde a disponibilidade importa mais que a consistência imediata (ex.: contador de likes), e evito onde não posso (ex.: saldo bancário).
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (caps. 2 modelos, 5 replicação, 6 particionamento, 9 consistência).
- **Reis & Housley — Fundamentals of Data Engineering** (sistemas de armazenamento NoSQL).
- **Documentação do MongoDB / Redis / Cassandra** (conceitos de cada família).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — modelos, replicação, CAP. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — armazenamento NoSQL. <!-- @reis2022 -->
- Tanimura, C. *SQL for Data Analysis* (2021) — o contraponto relacional. <!-- @tanimura2021 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
