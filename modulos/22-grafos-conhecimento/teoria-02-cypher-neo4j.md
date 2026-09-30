# Cypher e Neo4j: consultando grafos

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você entendeu *quando* usar grafos (unidade 1). Agora: como se **consulta** um grafo na prática? Em
SQL você descreve tabelas e JOINs; num grafo isso soa estranho. A resposta é uma linguagem feita
para conexões — **Cypher**, do **Neo4j** (o banco de grafos mais popular). O charme do Cypher é que
você **desenha o padrão** que procura, quase como um ASCII-art do grafo, e o banco encontra todas as
ocorrências. Saber ler e escrever Cypher básico é o "SQL dos grafos" — e é o que torna as travessias
da unidade 1 executáveis num banco real.

## 💡 Conceito (o porquê)

### Neo4j, em uma frase
**Neo4j** é um banco de dados de **property graph**: guarda nós e arestas com propriedades, e otimiza
a **travessia** (seguir relacionamentos é O(1) por aresta, não um JOIN). É consultado com **Cypher**.

### Cypher: você desenha o padrão
A ideia central do Cypher é **pattern matching** com uma sintaxe visual:
- **Nós** entre parênteses: `(p:Pessoa)` — variável `p`, rótulo `:Pessoa`.
- **Arestas** entre colchetes com setas: `-[:SEGUE]->` — tipo `:SEGUE`, direção `->`.
- Um **padrão** conecta os dois: `(a:Pessoa)-[:SEGUE]->(b:Pessoa)` — "a segue b".

O verbo `MATCH` procura esse padrão no grafo; `WHERE` filtra; `RETURN` devolve. É como se você
desenhasse o subgrafo que quer e o Neo4j preenchesse as variáveis com todas as combinações que batem.

### O básico (com paralelo ao SQL)
- **Criar:** `CREATE (:Pessoa {nome: 'Ana'})` — cria um nó. `CREATE (a)-[:SEGUE]->(b)` — cria aresta.
- **Ler:** `MATCH (p:Pessoa) WHERE p.nome = 'Ana' RETURN p` — o `SELECT ... WHERE` do grafo.
- **Relacionar:** `MATCH (a:Pessoa {nome:'Ana'})-[:SEGUE]->(b) RETURN b.nome` — quem Ana segue.
- **Agregar:** `MATCH (p)-[:SEGUE]->() RETURN p.nome, count(*)` — grau de saída de cada pessoa.

### A superpotência: travessia de profundidade variável
Aqui o Cypher faz o que o SQL não faz bem. Um `*` no relacionamento percorre **múltiplos saltos**:
- `MATCH (a)-[:SEGUE*1..3]->(b)` — b alcançável de a em **1 a 3 saltos** (amigos, amigos de amigos…).
- `MATCH caminho = shortestPath((a)-[:SEGUE*]->(b)) RETURN caminho` — o **caminho mais curto** entre a e b.

Aquelas perguntas que viravam JOINs infinitos (unidade 1) são **uma linha** em Cypher. É a diferença
que justifica um banco de grafos.

### Recomendação em uma consulta
O clássico "pessoas que você talvez conheça":
```cypher
MATCH (eu:Pessoa {nome:'Ana'})-[:SEGUE]->()-[:SEGUE]->(sugestao)
WHERE NOT (eu)-[:SEGUE]->(sugestao) AND sugestao <> eu
RETURN sugestao.nome, count(*) AS emComum
ORDER BY emComum DESC
```
Vizinhos-dos-vizinhos que eu ainda não sigo, ordenados por conexões em comum — a recomendação da
unidade 1, executável.

### Índices e desempenho
Como no relacional, você cria **índices** nas propriedades usadas para *entrar* no grafo (ex.:
`CREATE INDEX FOR (p:Pessoa) ON (p.nome)`) — para achar o nó inicial rápido. A partir daí, a
travessia é barata. O índice acelera o "ponto de partida"; o grafo acelera o "percurso".

## 🔎 Exemplo
Time de antifraude no Neo4j. Contas e transações são nós; `(:Conta)-[:TRANSFERIU]->(:Conta)`. Ao
marcar uma conta suspeita, a consulta `MATCH (s:Conta {flag:'suspeita'})-[:TRANSFERIU*1..4]-(c)
RETURN DISTINCT c` traz todas as contas conectadas em até 4 saltos — instantâneo. Com um índice em
`Conta(id)`, achar a conta inicial é imediato; a travessia de 4 saltos, que seria impraticável em
SQL, roda em milissegundos. Uma pergunta de negócio difícil virou uma linha de Cypher.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann apresenta o **Cypher** como a linguagem declarativa de consulta do modelo property graph,
contrastando-a com SQL e SPARQL, e destaca as consultas de **caminho de comprimento variável** como
o que os grafos fazem naturalmente e o relacional não. — *Designing Data-Intensive Applications*
(cap. 2).
:::

:::{admonition} 🏭 Do mundo real
:class: important
O padrão de recomendação e o de fraude em Cypher cabem em poucas linhas porque a travessia é nativa.
Na prática, cria-se índice nas propriedades de entrada (o "ponto de ancoragem" da consulta) e
deixa-se a engine percorrer as arestas. É a mesma disciplina do SQL (indexar o filtro), mas o
percurso profundo é onde o grafo ganha. — Kleppmann; docs do Neo4j.
:::

## ⚠️ Erros comuns
- **Escrever Cypher pensando em JOIN** — descreva o **padrão** (o desenho), não junções de tabelas.
- **Esquecer a direção** no `MATCH` (`->` vs `-`) — muda completamente o resultado.
- **Travessia sem limite** (`[:REL*]` irrestrito) em grafos enormes — pode explodir; limite a profundidade (`*1..4`).
- **Não indexar a propriedade de entrada** — a travessia é rápida, mas achar o nó inicial sem índice é lento.
- **Usar Neo4j para agregação tabular pesada** — para isso, warehouse colunar continua melhor.

## 💼 O que o mercado espera
Ler e escrever Cypher básico (`MATCH`/`WHERE`/`RETURN`, criação de nós/arestas), entender travessia
de profundidade variável (`*1..n`, `shortestPath`) e saber indexar a propriedade de entrada. Vagas
que mencionam Neo4j esperam esse nível; entrevistas de grafo pedem a consulta de recomendação/caminho.

:::{admonition} ✨ Em resumo
:class: resumo
- **Neo4j** = banco de property graph; **Cypher** = sua linguagem, baseada em **pattern matching** visual.
- Padrão: `(a:Pessoa)-[:SEGUE]->(b)`; verbos `MATCH` / `WHERE` / `RETURN` / `CREATE`.
- Superpotência: **profundidade variável** (`-[:REL*1..n]->`) e `shortestPath` — o que o SQL não faz bem.
- **Indexe a propriedade de entrada** para achar o nó inicial rápido; a travessia já é barata.
:::

## 🧠 Quiz de recall
1. Qual a ideia central do Cypher?
   :::{dropdown} Resposta
   Pattern matching: você "desenha" o padrão do grafo — nós `(x:Rotulo)` e arestas `-[:TIPO]->` — e o Neo4j encontra todas as ocorrências.
   :::
2. Como se escreve "Ana segue Bruno" em Cypher?
   :::{dropdown} Resposta
   Um padrão como `(a:Pessoa {nome:'Ana'})-[:SEGUE]->(b:Pessoa {nome:'Bruno'})`; com CREATE cria a aresta, com MATCH procura.
   :::
3. O que `-[:SEGUE*1..3]->` significa?
   :::{dropdown} Resposta
   Uma travessia de profundidade variável: alcançar o destino em 1 a 3 saltos seguindo arestas SEGUE — o que o SQL não expressa bem.
   :::
4. Como acelerar a entrada numa consulta de grafo?
   :::{dropdown} Resposta
   Criando um índice na propriedade usada para achar o nó inicial (ex.: `CREATE INDEX FOR (p:Pessoa) ON (p.nome)`); a travessia em si já é barata.
   :::
5. Quando NÃO usar Cypher/Neo4j?
   :::{dropdown} Resposta
   Para agregações tabulares pesadas (receita por mês etc.), onde um warehouse colunar é mais adequado; grafo brilha em travessias/conexões.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Escreva a consulta de recomendação 'quem seguir' em Cypher (em alto nível)."
  :::{dropdown} Resposta modelo
  `MATCH (eu {nome:'Ana'})-[:SEGUE]->()-[:SEGUE]->(sug) WHERE NOT (eu)-[:SEGUE]->(sug) AND sug<>eu RETURN sug.nome, count(*) AS emComum ORDER BY emComum DESC`. É uma travessia de 2 saltos (vizinhos dos vizinhos) filtrando quem já sigo, ordenada por conexões em comum. Cabe em uma consulta porque a travessia é nativa do grafo.
  :::
- **P:** "Como o Cypher difere do SQL na prática?"
  :::{dropdown} Resposta modelo
  No SQL eu descrevo tabelas e JOINs; no Cypher eu descrevo o padrão do grafo (o desenho de nós e arestas) e o banco casa o padrão. A grande diferença é a travessia de profundidade variável (`*1..n`, `shortestPath`), trivial no Cypher e sofrível no SQL. Ainda indexo a propriedade de entrada, como faria no relacional.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 2, Cypher e query de grafos).
- **Documentação do Neo4j / Cypher** — <https://neo4j.com/docs/>.
- **Reis & Housley — Fundamentals of Data Engineering** (bancos especializados na plataforma).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — Cypher e property graphs. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — bancos especializados. <!-- @reis2022 -->
- Robinson, I.; Webber, J.; Eifrem, E. *Graph Databases* (2ª ed., 2015) — Cypher e modelagem no Neo4j. <!-- @robinson2015 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
