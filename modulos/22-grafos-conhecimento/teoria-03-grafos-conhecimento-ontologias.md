# Grafos de conhecimento, ontologias e lineage

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Uma empresa tem "cliente" no CRM, "comprador" no e-commerce e "usuário" no app — três nomes para a
mesma coisa, em sistemas que não se falam. Como conectar tudo isso num modelo que uma máquina (e uma
pessoa) entenda, e sobre o qual dê para **inferir** ("se A é subsidiária de B, e B foi multada,
então A é parte relacionada")? A resposta é um **grafo de conhecimento**: um grafo que representa
não só dados, mas o **significado** e as **regras** de um domínio. É uma tendência forte em
plataformas de dados (a FIAP dedica um módulo a isso) e, mais perto de você, é exatamente a forma do
**lineage** de dados que você já usa. Esta unidade fecha o módulo ligando grafos ao significado e à
governança.

## 💡 Conceito (o porquê)

### O que é um grafo de conhecimento
Um **grafo de conhecimento (knowledge graph)** é um grafo que modela **entidades e as relações
semânticas entre elas** num domínio, de forma que o significado fique explícito e consultável. Não é
só "quem segue quem" — é "esta *empresa* **é subsidiária de** aquela", "este *produto* **pertence à
categoria** X", "este *dataset* **deriva de** aquele". Ele integra dados de várias fontes sob um
vocabulário comum e permite **consultar conhecimento**, não só registros.

### Triplas (RDF): sujeito–predicado–objeto
A forma canônica de representar conhecimento é a **tripla**: `(sujeito) -[predicado]-> (objeto)`.
- `(Ana) -[trabalha_em]-> (ACME)`
- `(ACME) -[é_subsidiária_de]-> (Holding)`

Cada fato é uma tripla; o conjunto de triplas é o grafo. É o modelo **RDF** (Resource Description
Framework), base da web semântica, consultado com **SPARQL** (o "SQL das triplas"). O property graph
(Neo4j, unidade 2) e o RDF são dois sabores da mesma ideia — nós e arestas com significado.

### Ontologias: o esquema do significado
Uma **ontologia** define o **vocabulário e as regras** do domínio: quais tipos de entidade existem
(`Pessoa`, `Empresa`), quais relações são válidas (`trabalha_em` liga `Pessoa`→`Empresa`), e
hierarquias (`Gerente` **é um** `Funcionário`). É o "esquema" de um grafo de conhecimento — e o que
permite **inferência**: se `Gerente é_um Funcionário` e `Ana é_um Gerente`, a máquina conclui que
`Ana é_um Funcionário` **sem que ninguém tenha escrito isso**. O conhecimento fica derivável, não só
armazenado.

### Resolução de entidades (o "cliente = comprador = usuário")
Um passo prático central: **entity resolution** — reconhecer que registros diferentes se referem à
**mesma entidade** e ligá-los no grafo. É o que unifica "cliente" (CRM), "comprador" (e-commerce) e
"usuário" (app) num único nó `Pessoa`, dando a visão 360°. Sem isso, o grafo de conhecimento é só
silos redesenhados.

### Onde você já usa isto: lineage como grafo de conhecimento
O **lineage de dados** (M14) é um grafo de conhecimento do seu próprio ambiente: nós são
datasets/colunas/jobs, arestas são `deriva_de` / `alimenta`. É o que responde "de onde veio este
número?" e "o que quebra se eu mudar esta tabela?" (impact analysis). O DAG do dbt/Airflow é
literalmente esse grafo. Modelar catálogo + lineage como grafo de conhecimento é o que plataformas
de governança (DataHub, etc.) fazem por baixo.

### Casos de uso típicos
- **Recomendação e busca semântica** (relacionar itens por significado, não só por texto).
- **Detecção de fraude** (anéis de contas conectadas — unidade 1).
- **Visão 360° de cliente** (unificar fontes via entity resolution).
- **Governança/lineage** (catálogo + proveniência como grafo).
- **Grafos como contexto para IA** (fora do nosso escopo agora, mas é para onde a FIAP aponta).

## 🔎 Exemplo
Uma empresa constrói um grafo de conhecimento corporativo. Uma **ontologia** define `Pessoa`,
`Empresa`, `Dataset` e relações (`trabalha_em`, `é_dono_de`, `deriva_de`). Por **entity resolution**,
o "cliente 123" do CRM e o "user_abc" do app viram o mesmo nó `Pessoa`. O **lineage** dos dados entra
como triplas `(fato_vendas) -[deriva_de]-> (stg_pedidos)`. Agora uma pergunta de governança —
"quais dashboards usam dado pessoal do cliente 123?" — vira uma travessia no grafo, cruzando pessoas,
datasets e lineage. O conhecimento espalhado em silos virou um grafo consultável e **inferível**.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann apresenta o modelo de **triplas (RDF)** e o SPARQL ao lado dos property graphs, como a base
para representar conhecimento ligado. Reis & Housley ligam **catálogo, lineage e metadados** à
governança — um grafo de conhecimento do próprio ambiente de dados. — *Designing Data-Intensive
Applications* (cap. 2); *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Plataformas de governança (DataHub, Amundsen, Neo4j-based catalogs) modelam catálogo + lineage como
**grafo de conhecimento**: é a forma natural de responder "de onde veio / para onde vai / quem é dono
/ o que é dado pessoal". Ou seja, você já vinha construindo um grafo de conhecimento sem chamar assim
— o lineage do M14. — Reis & Housley; prática de mercado.
:::

## ⚠️ Erros comuns
- **Grafo de conhecimento sem ontologia** — vira só um grafo de dados sem significado nem inferência.
- **Pular a resolução de entidades** — o mesmo cliente em 3 nós = silos redesenhados, sem visão 360°.
- **Confundir property graph com RDF** — são dois sabores; RDF/triplas é a base semântica clássica.
- **Modelar lineage à parte** quando ele já é um grafo de conhecimento do ambiente (reuse o conceito).
- **Achar que é só teoria** — recomendação, fraude, 360° e governança são casos concretos e comuns.

## 💼 O que o mercado espera
Explicar o que é um grafo de conhecimento (entidades + relações semânticas), triplas/RDF, o papel da
**ontologia** (vocabulário + inferência) e da **resolução de entidades**, e reconhecer que
lineage/catálogo são um grafo de conhecimento. É a linguagem de plataformas de governança e de dados
para IA.

:::{admonition} ✨ Em resumo
:class: resumo
- **Grafo de conhecimento** = grafo com **significado**: entidades e relações semânticas de um domínio.
- **Triplas (RDF)** `sujeito-predicado-objeto` (consultadas por SPARQL) são a forma canônica; property graph é o outro sabor.
- **Ontologia** define o vocabulário e habilita **inferência** (deduzir fatos não escritos); **entity resolution** unifica o mesmo ente de várias fontes.
- **Lineage/catálogo** (M14) já é um grafo de conhecimento do seu ambiente — a base da governança e da visão 360°.
:::

## 🧠 Quiz de recall
1. O que distingue um grafo de conhecimento de um grafo comum?
   :::{dropdown} Resposta
   Ele representa o significado do domínio — entidades e relações semânticas explícitas (e regras), permitindo consultar e inferir conhecimento, não só registros.
   :::
2. O que é uma tripla (RDF)?
   :::{dropdown} Resposta
   Um fato na forma sujeito–predicado–objeto (ex.: Ana –trabalha_em–> ACME); o conjunto de triplas forma o grafo, consultado com SPARQL.
   :::
3. Para que serve uma ontologia?
   :::{dropdown} Resposta
   Definir o vocabulário e as regras do domínio (tipos de entidade, relações válidas, hierarquias), habilitando inferência — deduzir fatos não escritos explicitamente.
   :::
4. O que é resolução de entidades e por que importa?
   :::{dropdown} Resposta
   Reconhecer que registros diferentes (cliente/comprador/usuário) são a mesma entidade e uni-los num nó; sem isso, o grafo é só silos redesenhados, sem visão 360°.
   :::
5. Como lineage se relaciona com grafos de conhecimento?
   :::{dropdown} Resposta
   O lineage (datasets/jobs ligados por deriva_de/alimenta) é um grafo de conhecimento do próprio ambiente de dados — base do impact analysis e da governança (M14).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "O que é um grafo de conhecimento e onde ele ajuda numa plataforma de dados?"
  :::{dropdown} Resposta modelo
  É um grafo que modela entidades e suas relações semânticas com significado explícito (via triplas/RDF ou property graph), geralmente sob uma ontologia que permite inferência. Ajuda em visão 360° de cliente (unificando fontes por entity resolution), recomendação/busca semântica, detecção de fraude e, muito concretamente, em governança: catálogo + lineage são um grafo de conhecimento que responde de onde veio o dado, quem é dono e o que é dado pessoal.
  :::
- **P:** "Qual a diferença entre property graph e RDF?"
  :::{dropdown} Resposta modelo
  São dois modelos de grafo. O property graph (Neo4j/Cypher) tem nós e arestas com propriedades, ótimo para travessias e aplicações. O RDF representa tudo como triplas sujeito-predicado-objeto, consultadas com SPARQL, e é a base clássica da web semântica e de ontologias/inferência. Ambos modelam conhecimento conectado; escolho pelo caso — property graph para app/travessia, RDF quando semântica/ontologia formal é central.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 2, triplas/RDF e SPARQL).
- **Reis & Housley — Fundamentals of Data Engineering** (metadados, catálogo e lineage).
- **W3C — RDF e SPARQL** (fundamentos da web semântica).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — triplas/RDF e SPARQL. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — metadados/lineage/governança. <!-- @reis2022 -->
- W3C. *RDF 1.1 Concepts and Abstract Syntax* (W3C Recommendation, 2014) — triplas e modelo RDF. <!-- @w3c-rdf11 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
