# Flashcards — Módulo 22

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Quando usar um banco de grafos? / **R:** Quando o relacionamento é o dado e as perguntas são travessias (amigos-de-amigos, caminhos, conexões a N saltos) — onde no relacional cada salto vira JOIN.
- **P:** O que é um property graph? / **R:** Grafo em que nós e arestas (com tipo e direção) carregam propriedades; o relacionamento é um objeto com dados, não só uma FK.
- **P:** Por que travessia profunda é cara no relacional? / **R:** Cada salto é um JOIN; muitos saltos degradam, e profundidade variável é difícil de expressar em SQL.
- **P:** Operações típicas de grafo? / **R:** Vizinhança/grau, caminho mais curto (BFS), componentes conexas, vizinhos em comum (recomendação).
- **P:** O que é o Cypher? / **R:** A linguagem do Neo4j baseada em pattern matching: você "desenha" o padrão `(a)-[:REL]->(b)` e o banco casa as ocorrências.
- **P:** Como escrever "Ana segue Bruno" em Cypher? / **R:** `(a:Pessoa {nome:'Ana'})-[:SEGUE]->(b:Pessoa {nome:'Bruno'})` (com CREATE cria, com MATCH busca).
- **P:** O que faz `-[:SEGUE*1..3]->`? / **R:** Travessia de profundidade variável: alcança o destino em 1 a 3 saltos — o que o SQL não faz bem.
- **P:** Como acelerar a entrada numa consulta de grafo? / **R:** Índice na propriedade usada para achar o nó inicial; a travessia em si já é barata.
- **P:** O que é um grafo de conhecimento? / **R:** Grafo com significado: entidades e relações semânticas de um domínio, permitindo consultar e inferir conhecimento.
- **P:** O que é uma tripla (RDF)? / **R:** Um fato sujeito-predicado-objeto (Ana –trabalha_em–> ACME); conjunto de triplas = grafo, consultado com SPARQL.
- **P:** Para que serve uma ontologia? / **R:** Definir vocabulário e regras do domínio e habilitar inferência (deduzir fatos não escritos).
- **P:** O que é resolução de entidades? / **R:** Reconhecer que registros diferentes (cliente/comprador/usuário) são a mesma entidade e uni-los num nó (visão 360°).
- **P:** Como lineage se relaciona a grafos? / **R:** Lineage (datasets/jobs ligados por deriva_de/alimenta) é um grafo de conhecimento do ambiente — base do impact analysis e da governança.

---
**Revisado em:** 2026-09-09
