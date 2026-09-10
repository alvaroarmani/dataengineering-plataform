# Índices por dentro e particionamento

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Uma consulta que era instantânea com mil linhas trava com dez milhões. O mesmo SQL, o mesmo banco —
o que mudou? Sem um **índice** adequado, o banco faz **full table scan**: lê a tabela inteira para
achar poucas linhas. A [teoria 05](teoria-05-indices-e-performance.md) mostrou *por que* indexar
(full scan vs índice, EXPLAIN); aqui descemos **um nível**: escolher o **tipo certo** de índice
(B-Tree/Hash/GIN/BRIN) e saber **particionar/shardear** tabelas gigantes — o que separa quem "escreve
SQL" de quem faz o banco **performar** (e custar menos, M21).

## 💡 Conceito (o porquê)

### O que um índice faz (e o custo)
Um **índice** é uma estrutura auxiliar que aponta para as linhas por uma coluna — como o índice
remissivo de um livro: em vez de folhear tudo, você vai direto. Acelera **leituras** com filtro/ordem
naquela coluna, mas **custa**: ocupa espaço e **torna as escritas mais lentas** (todo INSERT/UPDATE
atualiza o índice também). Regra: indexe o que você **filtra/junta/ordena** com frequência, não tudo.

### Os tipos de índice (Postgres) e quando usar
- **B-Tree** (o padrão, o coringa): mantém as chaves **ordenadas**. Serve para **igualdade** e,
  principalmente, **intervalos e ordenação** (`>`, `<`, `BETWEEN`, `ORDER BY`). 90% dos casos.
- **Hash:** otimizado só para **igualdade** (`=`). Rápido para "coluna = valor", mas não faz intervalo
  nem ordem.
- **GIN** (Generalized Inverted Index): para valores **compostos** — **texto (full-text)**, `JSONB`,
  arrays. É o índice de "esta palavra aparece neste documento?" (relaciona-se ao índice invertido, M18).
- **BRIN** (Block Range Index): minúsculo, para tabelas **enormes e naturalmente ordenadas** (ex.:
  append-only por data). Guarda o intervalo de valores por bloco; ideal para séries temporais gigantes
  onde um B-Tree seria caro demais.

Escolher o índice é escolher pela **forma da consulta**: igualdade → hash/btree; intervalo/ordem →
btree; texto/json → gin; tabela imensa por tempo → brin.

### Índices compostos e seletividade
Um índice **composto** (`(estado, cidade)`) serve consultas que filtram por `estado` ou por
`estado`+`cidade` — a **ordem das colunas importa** (ele ajuda `estado` sozinho, mas não `cidade`
sozinha). E índice só compensa em colunas **seletivas** (muitos valores distintos): indexar um
booleano (2 valores) raramente ajuda.

### Particionamento: quebrar a tabela grande
Quando uma tabela fica gigante, além de indexar, você a **particiona**: quebra-a em pedaços menores
por uma chave (tipicamente **data**: uma partição por mês). Benefícios:
- **Partition pruning:** uma consulta com filtro por data lê **só as partições relevantes**, pulando
  o resto — menos I/O, menos custo (M21). É o mesmo princípio do particionamento no BigQuery (M06).
- **Manutenção barata:** apagar dados velhos = dropar uma partição (instantâneo), em vez de um
  `DELETE` massivo.

### Sharding: distribuir entre máquinas
Particionamento divide dentro de **um** banco. **Sharding** distribui os pedaços entre **várias
máquinas** (M19) — para quando os dados/escrita passam do que um servidor aguenta. Cada shard guarda
um subconjunto (por hash ou intervalo da chave). Ganha escala horizontal; paga em complexidade
(consultas cross-shard, rebalanceamento).

## 🔎 Exemplo
Uma tabela `eventos(id, usuario_id, data, payload jsonb)` com 500 milhões de linhas. Você:
- Cria um **B-Tree** em `usuario_id` (filtra muito por usuário) e um índice **GIN** em `payload`
  (busca dentro do JSON).
- **Particiona** por mês na `data`: a consulta "eventos de março do usuário X" faz **partition
  pruning** (só a partição de março) + usa o índice de `usuario_id` — de minutos para milissegundos.
- Para o histórico frio de anos, um **BRIN** em `data` custa quase nada e ainda ajuda.
- Se um dia isso não couber num servidor, **shard** por `usuario_id` entre nós.
Mesma tabela, mesmas consultas — performáveis e baratas por design.

## ⚠️ Erros comuns
- **Indexar tudo** — cada índice pesa nas escritas e no espaço; indexe o que você filtra/ordena.
- **Índice errado para a consulta** — hash não faz intervalo; B-Tree não é ideal para full-text (use GIN).
- **Ordem errada no índice composto** — `(a, b)` não acelera filtro só por `b`.
- **Indexar coluna pouco seletiva** (booleano, poucos valores) — o banco ignora e faz scan.
- **Tabela gigante sem particionar** — full scans caros; particione por data e aproveite o pruning.

## 💼 O que o mercado espera
Escolher o índice certo pela consulta (B-Tree/Hash/GIN/BRIN), entender o custo de indexar, e saber
particionar tabelas grandes (partition pruning) e a noção de sharding. "Esta consulta está lenta, o
que você faz?" é pergunta clássica — a resposta começa em índice + particionamento.

:::{admonition} ✨ Em resumo
:class: resumo
- **Índice** acelera leitura filtrada/ordenada, mas custa espaço e **escrita** — indexe o que você consulta.
- **B-Tree** (intervalo/ordem, coringa) · **Hash** (só igualdade) · **GIN** (texto/JSON/array) · **BRIN** (tabela enorme ordenada por tempo).
- **Particionar** (por data) dá **partition pruning** (lê só o necessário) e manutenção barata.
- **Sharding** distribui entre máquinas (escala horizontal, M19) — mais complexo, para quando não cabe num servidor.
:::

## 🧠 Quiz de recall
1. Por que um índice acelera a leitura mas penaliza a escrita?
   :::{dropdown} Resposta
   Ele evita o full scan (vai direto às linhas), mas precisa ser atualizado a cada INSERT/UPDATE e ocupa espaço — então escritas ficam mais lentas.
   :::
2. Quando usar B-Tree, Hash, GIN e BRIN?
   :::{dropdown} Resposta
   B-Tree: intervalo/ordenação (e o coringa geral). Hash: só igualdade. GIN: texto/JSON/array (full-text). BRIN: tabelas enormes naturalmente ordenadas (ex.: por data).
   :::
3. O que é partition pruning?
   :::{dropdown} Resposta
   Quando a tabela é particionada (ex.: por mês), uma consulta com filtro naquela chave lê só as partições relevantes, pulando o resto — menos I/O e custo.
   :::
4. Por que a ordem das colunas num índice composto importa?
   :::{dropdown} Resposta
   Um índice `(a, b)` acelera filtros por `a` ou por `a`+`b`, mas não por `b` sozinho — ele é ordenado primeiro por `a`.
   :::
5. Qual a diferença entre particionamento e sharding?
   :::{dropdown} Resposta
   Particionamento divide a tabela dentro de um banco; sharding distribui os pedaços entre várias máquinas (escala horizontal, mais complexo).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Uma consulta ficou lenta conforme a tabela cresceu. Como você investiga e resolve?"
  :::{dropdown} Resposta modelo
  Olho o plano de execução (EXPLAIN) para ver se há full scan. Se filtro/ordeno por uma coluna sem índice, crio o índice do tipo certo — B-Tree para intervalo/ordem, hash para igualdade pura, GIN para texto/JSON. Confiro seletividade e a ordem de índices compostos. Se a tabela é enorme, particiono por data para aproveitar partition pruning, e considero BRIN para histórico. Se um servidor não dá conta, penso em sharding.
  :::
- **P:** "Quando NÃO criar um índice?"
  :::{dropdown} Resposta modelo
  Em colunas pouco seletivas (poucos valores distintos, como um booleano), onde o banco vai ignorá-lo; ou em tabelas com escrita muito intensa e leitura rara, onde o custo de manter o índice não compensa. Índice não é de graça: pesa em espaço e em cada escrita.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 3, storage e índices).
- **Documentação do PostgreSQL — Indexes** (B-Tree/Hash/GIN/BRIN, partitioning).
- **Tanimura — SQL for Data Analysis** (consultas e performance).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — estruturas de índice. <!-- @kleppmann2017 -->
- Tanimura, C. *SQL for Data Analysis* (2021) — consultas e desempenho. <!-- @tanimura2021 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
