# Por que grafos? Quando o relacionamento é o dado

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Algumas perguntas são um pesadelo em SQL: "quais amigos dos meus amigos eu ainda não sigo?", "qual
o caminho de aprovação entre este funcionário e o CEO?", "que contas estão conectadas a esta fraude
por até 4 saltos?". No modelo relacional, cada "salto" vira um **JOIN**, e perguntas de
profundidade variável viram consultas monstruosas (ou impossíveis). O problema é que, nesses casos,
**o relacionamento É o dado** — e o banco relacional trata relacionamento como coisa secundária
(uma FK). **Bancos de grafos** invertem isso: conexões são cidadãos de primeira classe. Entender
quando usar um grafo — e quando não — é uma competência que aparece em plataformas de dados
modernas (recomendação, detecção de fraude, lineage, grafos de conhecimento).

## 💡 Conceito (o porquê)

### O modelo de propriedades (property graph)
Um grafo tem duas peças:
- **Nós (vertices):** as entidades (uma pessoa, um produto, uma conta), com um rótulo (`:Pessoa`) e
  **propriedades** (nome, idade).
- **Arestas (edges/relationships):** as conexões entre nós, com um **tipo** (`:SEGUE`, `:COMPROU`),
  uma **direção** e também **propriedades** (desde quando, peso).

É o **property graph** (usado por Neo4j). Tudo que interessa — inclusive o relacionamento — carrega
dados. Uma "amizade" não é uma linha numa tabela de junção; é uma aresta com atributos próprios.

### Por que não usar só o relacional
Você *pode* modelar relacionamentos com tabelas de junção e FKs. O problema aparece em **consultas
de travessia** (percorrer muitos saltos):
- Cada salto exige um **JOIN**; "amigos dos amigos dos amigos" = 3 self-joins, e a performance
  degrada rápido.
- Perguntas de **profundidade variável** ("qualquer caminho entre A e B") são difíceis ou
  impossíveis de expressar em SQL padrão.

Num banco de grafos, seguir uma aresta é uma operação **direta e barata** (o nó "aponta" para o
vizinho), então travessias profundas são naturais e rápidas. É a diferença entre *calcular* as
conexões toda vez (JOIN) e *já tê-las* materializadas como arestas.

### Grafos dirigidos e não-dirigidos
- **Dirigido:** a aresta tem sentido (`ana -SEGUE-> bruno` ≠ `bruno -SEGUE-> ana`). Redes sociais,
  dependências, lineage.
- **Não-dirigido:** a conexão é mútua (`ana -AMIGO- bruno`). Amizades, coautoria.

O sentido muda as perguntas: "quem **eu** sigo" vs "quem me **segue**".

### Operações típicas de grafo
As perguntas que grafos respondem bem:
- **Vizinhança e grau:** quem está diretamente conectado; quão conectado um nó é (centralidade).
- **Caminho mais curto:** menor nº de saltos entre dois nós (BFS) — "graus de separação".
- **Componentes conexas:** grupos de nós todos alcançáveis entre si (comunidades).
- **Vizinhos em comum:** base de recomendação ("pessoas que talvez você conheça").

### RDF/triplas e grafos de conhecimento (panorama)
Além do property graph, existe o modelo **RDF** (triplas *sujeito–predicado–objeto*), base dos
**grafos de conhecimento** e da web semântica (consultados com SPARQL). É o que estrutura ontologias
e conhecimento ligado — tema da unidade 3.

## 🔎 Exemplo
Uma rede social guarda `(:Pessoa)-[:SEGUE]->(:Pessoa)`. Para "sugerir quem seguir", a pergunta é:
*vizinhos dos meus vizinhos que eu ainda não sigo*. Num grafo, isso é uma travessia de 2 saltos,
direta e rápida. No relacional, seriam dois JOINs na tabela `segue` + um anti-join para excluir quem
já sigo — que degrada conforme a rede cresce. Para "detectar fraude", a mesma engine acha **contas a
até 4 saltos** de uma conta marcada — uma travessia de profundidade variável, trivial no grafo e
sofrível no SQL. O relacionamento deixou de ser um JOIN e virou o próprio objeto da consulta.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann dedica uma seção aos **modelos de dados de grafo** — property graphs, o modelo de triplas
(RDF) e as linguagens de consulta (Cypher, SPARQL) — mostrando por que grafos brilham em dados
altamente conectados onde o relacional sofre com JOINs. — *Designing Data-Intensive Applications*
(cap. 2, "Graph-Like Data Models").
:::

:::{admonition} 🏭 Do mundo real
:class: important
Grafos são a espinha de recomendação (LinkedIn "pessoas que você talvez conheça"), detecção de
fraude (conexões suspeitas entre contas), e **lineage de dados** (o próprio DAG do dbt/Airflow é um
grafo dirigido!). A regra: use grafo quando as **conexões e travessias** são o foco; mantenha o
relacional quando o foco é agregação tabular. — Kleppmann; prática de mercado.
:::

## ⚠️ Erros comuns
- **Usar grafo para tudo** — para agregações tabulares ("receita por mês"), o relacional/colunar é melhor.
- **Modelar travessia profunda com JOINs** no relacional — vira consulta monstruosa e lenta.
- **Ignorar a direção das arestas** — "quem sigo" ≠ "quem me segue"; a direção define a pergunta.
- **Achar que grafo = só visualização** — o valor é a travessia eficiente, não o desenho bonito.
- **Esquecer que o DAG que você já usa (dbt/Airflow) é um grafo** — lineage é um problema de grafo.

## 💼 O que o mercado espera
Reconhecer quando o problema é de grafo (dados altamente conectados, travessias de profundidade
variável), explicar o property graph (nós/arestas com propriedades) e as operações típicas
(vizinhança, caminho mais curto, componentes). Aparece em system design de recomendação/fraude/lineage.

:::{admonition} ✨ Em resumo
:class: resumo
- Use grafo quando **o relacionamento é o dado** e as perguntas são **travessias** (amigos-de-amigos, caminhos, fraude).
- **Property graph**: nós e **arestas** carregam propriedades; seguir uma aresta é direto e barato (≠ JOIN).
- No relacional, cada salto é um JOIN; profundidade variável é difícil/inviável.
- Operações típicas: vizinhança/grau, **caminho mais curto (BFS)**, componentes conexas, vizinhos em comum. RDF/triplas = base dos grafos de conhecimento.
:::

## 🧠 Quiz de recall
1. Quando um grafo é melhor que o modelo relacional?
   :::{dropdown} Resposta
   Quando os dados são altamente conectados e as perguntas são travessias (amigos-de-amigos, caminhos, conexões a N saltos) — onde cada salto no relacional vira um JOIN caro.
   :::
2. O que é um property graph?
   :::{dropdown} Resposta
   Um grafo em que nós (entidades) e arestas (relacionamentos, com tipo e direção) carregam propriedades. O relacionamento é um objeto com dados, não só uma FK.
   :::
3. Por que travessias profundas são caras no relacional?
   :::{dropdown} Resposta
   Cada salto exige um JOIN; muitos saltos = muitos self-joins que degradam a performance, e profundidade variável é difícil de expressar em SQL padrão.
   :::
4. Cite três operações típicas de grafo.
   :::{dropdown} Resposta
   Vizinhança/grau (centralidade), caminho mais curto (BFS, "graus de separação") e componentes conexas; também vizinhos em comum (recomendação).
   :::
5. Por que a direção das arestas importa?
   :::{dropdown} Resposta
   Ela define a pergunta: em um grafo dirigido, "quem eu sigo" (arestas saindo) é diferente de "quem me segue" (arestas chegando).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Quando você escolheria um banco de grafos em vez de um relacional?"
  :::{dropdown} Resposta modelo
  Quando o relacionamento é o foco e preciso de travessias — recomendação (amigos de amigos), fraude (conexões a N saltos), lineage. No grafo, seguir arestas é direto e barato, e profundidade variável é natural; no relacional isso vira uma cascata de JOINs que degrada. Para agregações tabulares clássicas, fico no relacional/colunar. Escolho pela forma da pergunta, não por moda.
  :::
- **P:** "Como você modelaria 'pessoas que você talvez conheça'?"
  :::{dropdown} Resposta modelo
  Como um grafo `(:Pessoa)-[:SEGUE]->(:Pessoa)`. A sugestão é uma travessia de 2 saltos: vizinhos dos meus vizinhos que eu ainda não sigo, opcionalmente ordenados por quantidade de amigos em comum (força da conexão). É direto no grafo; no relacional exigiria dois JOINs na tabela de relações mais um anti-join, escalando mal.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 2, modelos de dados de grafo).
- **Documentação do Neo4j** — modelo de property graph.
- **Reis & Housley — Fundamentals of Data Engineering** (modelos de dados na plataforma).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 2, graph data models. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — modelos de dados. <!-- @reis2022 -->
- Robinson, I.; Webber, J.; Eifrem, E. *Graph Databases* (2ª ed., 2015) — property graph e quando usar grafos. <!-- @robinson2015 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
