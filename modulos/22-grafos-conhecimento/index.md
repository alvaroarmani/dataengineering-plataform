# Módulo 22 — Grafos de Conhecimento e Bancos de Grafos

> Quando o **relacionamento é o dado**: bancos de grafos (Neo4j/Cypher), travessias que o SQL não
> faz bem, e grafos de conhecimento (ontologias, lineage). Um paradigma de dados que o mercado pede
> em recomendação, fraude e governança.

## Identificação
- **Eixo:** 1 — Fundamentos
- **Carga horária:** 25h
- **Pré-requisitos:** M04 (SQL), M18 (NoSQL)
- **Onde roda:** 🟢 Browser (algoritmos de grafo em Python) + 🐳 Neo4j na bancada (guiado)

## Ementa
Modelo de grafos e quando usá-lo vs relacional (o relacionamento como cidadão de primeira classe;
travessias vs JOINs). **Property graph** e **Neo4j/Cypher**: nós, arestas, pattern matching,
travessia de profundidade variável e caminho mais curto. Algoritmos: vizinhança, grau/centralidade,
BFS, componentes conexas, recomendação por vizinhos em comum. **Grafos de conhecimento**: triplas
(RDF), SPARQL, **ontologias** e inferência, resolução de entidades, e lineage/catálogo como grafo.

## Competências e habilidades
- C20 — modelar e consultar dados como grafo; reconhecer casos de grafo de conhecimento.

## Objetivos de aprendizagem
1. **Decidir** entre grafo e relacional a partir da forma da pergunta.
2. **Aplicar** algoritmos de grafo (vizinhança, BFS, componentes, recomendação).
3. **Ler/escrever** Cypher básico (incl. travessia de profundidade variável).
4. **Explicar** grafos de conhecimento (triplas/RDF, ontologias, entity resolution) e a ligação com lineage.

## Plano de aulas (unidades)

**Unidade 1 — Por que grafos? Modelo e algoritmos**
1. **Teoria:** [Por que grafos? Quando o relacionamento é o dado](teoria-01-por-que-grafos.md)
2. **Exercícios:** [Da tabela de arestas ao grafo (🟢)](exercicio-01.md) · [Graus: fontes e sumidouros do lineage (🟢)](exercicio-02.md) · [Caminho mais curto e k saltos / BFS (🟢)](exercicio-03.md)

**Unidade 2 — Cypher e Neo4j**
1. **Teoria:** [Cypher e Neo4j: consultando grafos](teoria-02-cypher-neo4j.md)
2. **Exercícios:** [Recomendação por amigos em comum (🟢)](exercicio-04.md) · [Centralidade: os hubs da rede (🟢)](exercicio-05.md)

**Unidade 3 — Grafos de conhecimento**
1. **Teoria:** [Grafos de conhecimento, ontologias e lineage](teoria-03-grafos-conhecimento-ontologias.md)
2. **Exercícios:** [Resolução de entidades com componentes conexas (🟢)](exercicio-06.md)

> **Módulo completo.** O terceiro modelo de dados do curso (relacional M04 · NoSQL M18 · **grafos**).

## Metodologia e avaliação
**Maestria:** decidir grafo vs relacional para casos dados, resolver os algoritmos de grafo e ler/
escrever Cypher básico — conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Reconhecer problemas de grafo (recomendação, fraude, lineage) e ter noção de Neo4j/Cypher é
diferencial; grafos de conhecimento aparecem em plataformas de governança e de dados modernas.

## Erros comuns
- Usar grafo para agregação tabular (o relacional/colunar é melhor).
- Modelar travessia profunda com JOINs.
- Ignorar a direção das arestas.
- Grafo de conhecimento sem ontologia / sem resolução de entidades.

## Recursos
Ver [`recursos.md`](recursos.md) (Kleppmann cap. 2; docs Neo4j/Cypher; RDF/SPARQL).

---
**Revisado em:** 2026-09-09
