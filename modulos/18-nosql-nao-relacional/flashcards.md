# Flashcards — Módulo 18

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** NoSQL substitui SQL? / **R:** Não; complementa. Cada família troca garantias (esquema/JOIN/ACID) por escala, flexibilidade ou velocidade. Escolha pelo padrão de acesso.
- **P:** As quatro famílias NoSQL? / **R:** Documento (Mongo), key-value (Redis), wide-column (Cassandra), grafo (Neo4j) — + série temporal.
- **P:** Schema-on-write vs schema-on-read? / **R:** Write (relacional): esquema antes, recusa fora dele. Read (NoSQL): grava flexível, a aplicação interpreta na leitura.
- **P:** O que diz o teorema CAP? / **R:** Sob partição de rede (P), escolha entre consistência (C) e disponibilidade (A). Muitos NoSQL escolhem A com consistência eventual.
- **P:** Por que desnormalizar em NoSQL? / **R:** Não há JOIN distribuído eficiente; modela-se pela consulta e duplica-se o dado para ler rápido e escalar.
- **P:** Documento: embutir vs referenciar? / **R:** Embutir o que se lê junto e é limitado; referenciar (só o id) o que é grande, volátil ou compartilhado.
- **P:** Para que serve o pipeline de agregação? / **R:** Encadear estágios (match/group/sort) para análises sobre documentos — o GROUP BY do NoSQL documento.
- **P:** Caso de uso e traço-chave do Redis? / **R:** Cache/sessão/contador; key-value em memória, latência mínima, com TTL. Busca só por chave; é efêmero.
- **P:** Padrão cache-aside? / **R:** App busca no cache; no miss, vai ao banco, grava no cache com TTL e devolve; próximas leituras vêm do cache até expirar.
- **P:** Cassandra é bom para quê? / **R:** Escrita massiva e escala horizontal (masterless), com consistência ajustável.
- **P:** Partition key vs clustering key? / **R:** Partition key decide o nó (localidade); clustering key ordena dentro da partição (ex.: por tempo).
- **P:** Modelar "pela consulta"? / **R:** Desenhar chaves (e duplicar tabelas) em torno da pergunta, pois não há JOIN nem ad-hoc eficiente em Cassandra.
- **P:** O que é downsampling em série temporal? / **R:** Agregar dados antigos em janelas maiores (min→hora→dia) e descartar a alta resolução, para o volume não crescer sem limite.
- **P:** Regra do quórum para leitura consistente? / **R:** R + W > N garante interseção entre quem escreveu e quem lê (leitura vê a última escrita).

---
**Revisado em:** 2026-08-31
