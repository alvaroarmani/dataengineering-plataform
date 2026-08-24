# Por que o DW é rápido: colunar, compressão, particionamento e clustering

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Uma consulta analítica típica — "receita total por mês em 2025" — precisa de **poucas
colunas** (data e valor) mas **muitas linhas**. Num banco de linhas (OLTP), o motor lê a
linha inteira de cada registro, desperdiçando I/O com colunas que a query nem usa. Os DWs
resolvem isso com um conjunto de técnicas de armazenamento: **colunar + compressão +
particionamento + clustering**. Entendê-las é o que separa "sei escrever SQL" de "sei fazer
o DW voar (e barato)".

## 💡 Conceito (o porquê)

### Armazenamento colunar
Em vez de guardar linha a linha, o DW guarda **coluna a coluna**: todos os valores de `valor`
juntos, todos os de `data` juntos. Consequências enormes para análise:

- **Lê só as colunas necessárias.** `SELECT data, valor` não toca nas outras 30 colunas — I/O
  proporcional ao que você usa, não ao tamanho da linha.
- **Compressão muito melhor.** Valores de uma mesma coluna são homogêneos (mesmo tipo,
  valores parecidos), então comprimem muito mais que uma linha heterogênea.
- **Execução vetorizada.** O motor processa blocos de uma coluna de uma vez, aproveitando a CPU.

É por isso que `SELECT *` é um pecado no DW: força ler **todas** as colunas.

### Compressão
Sobre os dados colunares, o DW aplica esquemas como:

- **Dictionary encoding:** valores repetidos (ex.: `estado`) viram um dicionário + códigos curtos.
- **Run-length encoding (RLE):** sequências repetidas viram "(valor, quantidade)" — poderoso
  quando os dados estão **ordenados**.

Menos bytes no disco = menos I/O = consulta mais rápida **e** mais barata (em DWs cloud você
paga por bytes lidos).

### Particionamento
Divide fisicamente a tabela por uma coluna — tipicamente **data** (ex.: uma partição por dia
ou mês). Ao filtrar `WHERE data >= '2025-01-01'`, o motor **pula (prune)** as partições fora
do intervalo, lendo só as relevantes. Filtrar pela **coluna de partição** é o maior ganho de
performance/custo num DW.

### Clustering / ordenação
Dentro da partição, **ordena os dados** por colunas muito filtradas (ex.: `categoria`). O DW
guarda o **mín/máx de cada bloco**; ao filtrar `WHERE categoria = 'livros'`, ele pula blocos
cujo intervalo não contém o valor (*block/zone pruning*). Complementa o particionamento para
filtros em colunas de alta seletividade.

```{mermaid}
flowchart TB
    Q["SELECT valor WHERE data em 2025 AND categoria='livros'"] --> P{Particionamento<br/>pula anos != 2025}
    P --> C{Clustering<br/>pula blocos sem 'livros'}
    C --> R[Lê só o mínimo necessário]
```

## 🔎 Exemplo
Uma tabela de 2 bilhões de linhas, particionada por mês e clusterizada por `categoria`. A
query "receita de livros em jan/2025": o particionamento descarta 59 dos 60 meses; o
clustering descarta os blocos sem 'livros'; o colunar lê só `valor`. Resultado: varre uma
fração ínfima dos dados — rápido e barato — em vez da tabela inteira.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann dedica uma seção ao armazenamento orientado a colunas: separar as colunas permite
ler só o necessário e **comprimir muito melhor** (dictionary e bitmap/RLE), e **ordenar os
dados** amplifica a compressão e o *pruning*. É a base técnica de todo DW analítico moderno.
— *Designing Data-Intensive Applications*, cap. 3.
:::

:::{admonition} 🏭 Do mundo real
:class: important
No BigQuery, particionar por data e clusterizar por colunas muito filtradas reduz
drasticamente os **bytes varridos** — e como a cobrança é por bytes lidos na consulta, isso
vira **economia direta**. A documentação recomenda ambos para tabelas grandes. —
BigQuery, documentação oficial (partitioning & clustering).
:::

## ⚠️ Erros comuns
- **`SELECT *`** numa tabela larga/grande — lê todas as colunas e (no cloud) infla o custo.
- **Não filtrar pela coluna de partição** — anula o *partition pruning* (varre tudo).
- Aplicar uma função na coluna de partição no filtro (ex.: `WHERE CAST(data AS ...) = ...`) —
  costuma **impedir** o pruning.
- Particionar por uma coluna de **altíssima cardinalidade** (ex.: `id`) — cria partições
  demais e piora tudo.
- Confundir **particionamento** (divide a tabela) com **clustering** (ordena dentro dela) —
  são complementares.

## 💼 O que o mercado espera
"Por que o colunar é rápido para análise?" e "como você reduziria o custo/latência de uma
query no BigQuery?" são perguntas frequentes. Consciência de **custo por bytes varridos** é
das habilidades mais valorizadas em quem trabalha com DW cloud.

:::{admonition} ✨ Em resumo
:class: resumo
- **Colunar** lê só as colunas usadas e comprime muito melhor — por isso evite `SELECT *`.
- **Compressão** (dictionary, RLE) reduz bytes ⇒ mais rápido e mais barato (paga-se por bytes lidos).
- **Particionamento** divide por data e permite **pular partições** ao filtrar pela coluna de partição.
- **Clustering** ordena dentro da partição e pula blocos por mín/máx — complementa o particionamento.
:::

## 🧠 Quiz de recall
1. Por que o armazenamento colunar acelera consultas analíticas?
   :::{dropdown} Resposta
   Porque guarda cada coluna separadamente: lê só as colunas usadas (menos I/O), comprime muito melhor (dados homogêneos) e permite execução vetorizada.
   :::
2. Por que `SELECT *` é ruim num DW?
   :::{dropdown} Resposta
   Força ler todas as colunas do armazenamento colunar, aumentando I/O e (no cloud) o custo, mesmo que a análise use poucas colunas.
   :::
3. O que é partition pruning?
   :::{dropdown} Resposta
   Quando o motor pula (não lê) as partições fora do filtro. Ocorre ao filtrar pela coluna de partição (tipicamente data), reduzindo muito os dados varridos.
   :::
4. Qual a diferença entre particionamento e clustering?
   :::{dropdown} Resposta
   Particionamento divide fisicamente a tabela (ex.: por mês); clustering ordena os dados dentro da partição por colunas muito filtradas, permitindo pular blocos por mín/máx. São complementares.
   :::
5. Cite dois esquemas de compressão comuns e quando brilham.
   :::{dropdown} Resposta
   Dictionary encoding (valores repetidos → dicionário + códigos) e run-length encoding/RLE (sequências repetidas → valor+contagem), que brilha quando os dados estão ordenados.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Uma query no BigQuery está lenta e cara. O que você investiga primeiro?"
  :::{dropdown} Resposta modelo
  Se há `SELECT *` (troco por só as colunas necessárias), se o filtro usa a coluna de partição (para habilitar pruning) e sem função em cima dela, e se a tabela está particionada por data e clusterizada pelas colunas mais filtradas. Confiro a estimativa de bytes varridos antes de rodar.
  :::
- **P:** "Por que colunar comprime melhor que linhas?"
  :::{dropdown} Resposta modelo
  Porque numa coluna os valores são homogêneos (mesmo tipo, distribuição parecida), o que casa com dictionary/RLE; numa linha os campos são heterogêneos e comprimem pouco. Ordenar os dados melhora ainda mais o RLE.
  :::
- **P:** "Quando NÃO particionar por uma coluna?"
  :::{dropdown} Resposta modelo
  Quando ela tem cardinalidade altíssima (ex.: um id único), pois geraria partições demais (overhead) — o oposto do ganho. Particiona-se por colunas de baixa/média cardinalidade e muito usadas em filtro, como data.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications**, cap. 3 (column-oriented storage, compressão, sort order).
- **Reis & Housley — Fundamentals of Data Engineering**, cap. 6 (armazenamento).
- **BigQuery docs** — Partitioned tables & Clustered tables.

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 3 (armazenamento colunar, compressão, ordenação). <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 6 (armazenamento). <!-- @reis2022 -->
- BigQuery — Documentação oficial (particionamento e clustering). <!-- @docs-bigquery -->

*Acessado em: 2026-08-23.*

---
**Revisado em:** 2026-08-23
