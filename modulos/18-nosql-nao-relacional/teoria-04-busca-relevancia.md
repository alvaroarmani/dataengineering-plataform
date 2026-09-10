# Busca e relevância: índice invertido, TF-IDF e BM25

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

"Buscar produtos que mencionam *fone bluetooth*" parece trivial — até você tentar com `LIKE
'%fone%'` num banco relacional e descobrir que é lento (full scan), burro (não entende relevância,
plural, acentos) e não ordena por "o quê importa mais". Busca de texto é um problema **próprio**, e é
o que motiva sistemas como **Elasticsearch/OpenSearch** e os recursos de busca do **MongoDB** (que a
FIAP cobre em NoSQL). No centro estão duas ideias que todo engenheiro de dados deveria conhecer: o
**índice invertido** (como achar documentos rápido) e o **ranqueamento por relevância** (TF-IDF/BM25
— como ordenar os resultados). É o que transforma "encontrar" em "encontrar o melhor".

## 💡 Conceito (o porquê)

### Por que `LIKE` não é busca
`WHERE texto LIKE '%fone%'` faz **full scan** (o `%` inicial impede índice comum), casa apenas
substring literal (não entende relevância, radical, sinônimo) e **não ordena** por importância.
Funciona para achar; falha para **buscar bem**. Busca de verdade precisa de estrutura própria.

### O índice invertido: a estrutura da busca
Um **índice invertido** mapeia **cada termo → a lista de documentos que o contêm**:
```
"gato"  -> [doc1, doc2]
"preto" -> [doc1]
```
É o "inverso" de um documento (que lista seus termos). Para buscar "gato", você **vai direto** à
lista de docs — não varre nada. É exatamente como o índice remissivo de um livro, e é o que o **GIN**
do Postgres (M04) e os motores de busca usam por baixo. Construir um índice invertido é: para cada
documento, para cada termo (tokenizado, minúsculo), adicionar o doc à lista daquele termo.

### Análise de texto: tokenização e normalização
Antes de indexar, o texto passa por **análise**: quebrar em **tokens** (palavras), pôr em minúsculas,
remover acentos e **stop words** ("de", "a", "o"), e aplicar **stemming** (reduzir ao radical:
"correndo"→"corr") para que "corre", "correndo", "correu" batam. Sem isso, a busca fica literal e
frágil. É o pré-processamento que faz "fones" achar "fone".

### Ranqueamento: TF-IDF
Achar os documentos é metade; **ordená-los por relevância** é a outra. O clássico é o **TF-IDF**:
- **TF (Term Frequency):** quanto mais vezes o termo aparece **no documento**, mais relevante ele é
  para aquele termo.
- **IDF (Inverse Document Frequency):** termos que aparecem em **muitos** documentos (comuns) valem
  **menos**; termos raros valem mais. "bluetooth" discrimina mais que "produto".
- O score combina os dois: **frequente no documento, raro no acervo** = muito relevante.

### BM25: o padrão moderno
O **BM25** é o TF-IDF **melhorado**, hoje o padrão de fato (Elasticsearch, Lucene). Dois ajustes que
importam: **saturação do TF** (a 10ª ocorrência de um termo agrega menos que a 2ª — retornos
decrescentes) e **normalização pelo tamanho do documento** (um termo num texto curto conta mais que
o mesmo termo perdido num texto enorme). O resultado ranqueia de forma mais justa que o TF-IDF puro.

### Onde isso vive
Busca full-text aparece em: **Elasticsearch/OpenSearch** (motores dedicados), **MongoDB Atlas Search**
e o `$text`/índices de texto do Mongo (NoSQL documento, M18), e o **GIN + tsvector** do Postgres
(M04) para casos mais simples. A escolha é de escala: Postgres/GIN resolve busca modesta; um motor
dedicado (Elastic) entra quando busca é o produto.

## 🔎 Exemplo
Um e-commerce indexa descrições de produtos. A **análise** tokeniza e aplica stemming
("fones"→"fone"). O **índice invertido** mapeia `fone -> [p1, p3, p7]`, `bluetooth -> [p3, p7]`. A
busca "fone bluetooth" intersecta as listas → candidatos p3, p7 — **instantâneo**, sem scan. O
**BM25** ranqueia: p3, que tem "bluetooth" (termo raro) no título curto, vence p7, onde o termo
aparece uma vez num texto longo. O usuário vê primeiro o resultado mais relevante — não só "um que
contém as palavras". Impossível de fazer bem com `LIKE`.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann descreve **índices de busca full-text** (índices invertidos como os do Lucene) como uma
categoria de estrutura de dados de armazenamento, distinta dos índices B-Tree/LSM transacionais.
Reis & Housley situam bancos de busca entre os armazenamentos especializados que o engenheiro escolhe
por caso de uso. — *Designing Data-Intensive Applications* (cap. 3); *Fundamentals of Data
Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Toda barra de busca decente (e-commerce, docs, logs) roda sobre índice invertido + ranqueamento
BM25, tipicamente em Elasticsearch/OpenSearch. O erro clássico de iniciante é tentar resolver busca
com `LIKE '%x%'` no banco transacional — funciona no protótipo e desmorona em escala e qualidade. —
Kleppmann; prática de mercado.
:::

## ⚠️ Erros comuns
- **Usar `LIKE '%x%'` como busca** — full scan, sem relevância, sem stemming; não escala.
- **Pular a análise de texto** — sem tokenização/stemming/stop words, a busca fica literal e frágil.
- **Ordenar só por TF** — sem IDF, termos comuns dominam; sem normalização, textos longos enganam (use BM25).
- **Elasticsearch para tudo** — para busca modesta, GIN/`tsvector` do Postgres basta; motor dedicado tem custo operacional.
- **Confundir achar com ranquear** — o índice invertido acha; TF-IDF/BM25 ordena por relevância.

## 💼 O que o mercado espera
Entender por que `LIKE` não é busca, o que é um índice invertido, a análise de texto (tokenização/
stemming/stop words) e o ranqueamento (TF-IDF, BM25), sabendo onde roda (Elasticsearch, Mongo Search,
GIN do Postgres). Aparece quando o produto tem busca ou quando se discute NoSQL documento/search.

:::{admonition} ✨ Em resumo
:class: resumo
- **`LIKE '%x%'` não é busca**: full scan, literal, sem relevância. Busca precisa de estrutura própria.
- **Índice invertido** (termo → docs) acha documentos sem varrer; é o coração dos motores de busca (e do GIN).
- **Análise de texto** (tokenizar, minúsculas, stop words, stemming) faz "fones" achar "fone".
- **Ranqueamento**: **TF-IDF** (frequente no doc, raro no acervo) e **BM25** (com saturação de TF e normalização por tamanho) ordenam por relevância.
:::

## 🧠 Quiz de recall
1. Por que `LIKE '%termo%'` não serve como busca de verdade?
   :::{dropdown} Resposta
   Faz full scan (o % inicial impede índice), casa só substring literal (sem relevância/stemming/sinônimo) e não ordena por importância.
   :::
2. O que é um índice invertido?
   :::{dropdown} Resposta
   Uma estrutura que mapeia cada termo à lista de documentos que o contêm, permitindo achar documentos por termo sem varrer o acervo.
   :::
3. Para que serve a análise de texto antes de indexar?
   :::{dropdown} Resposta
   Tokenizar, normalizar (minúsculas, acentos), remover stop words e aplicar stemming — para que variações da palavra (fone/fones) casem e a busca não seja literal.
   :::
4. O que TF e IDF medem no TF-IDF?
   :::{dropdown} Resposta
   TF: frequência do termo no documento (mais = mais relevante). IDF: raridade do termo no acervo (termos comuns valem menos). O score combina: frequente no doc e raro no acervo.
   :::
5. O que o BM25 melhora em relação ao TF-IDF?
   :::{dropdown} Resposta
   Satura o TF (ocorrências extras agregam cada vez menos) e normaliza pelo tamanho do documento (um termo num texto curto conta mais que num longo), ranqueando de forma mais justa.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você implementaria uma busca de produtos por texto?"
  :::{dropdown} Resposta modelo
  Não com `LIKE`. Usaria um índice invertido com análise de texto (tokenização, minúsculas, remoção de acentos/stop words, stemming) e ranqueamento por BM25. Para escala/qualidade, um motor dedicado como Elasticsearch/OpenSearch (ou Mongo Atlas Search); para busca modesta, o GIN + tsvector do Postgres resolve. O índice invertido acha os candidatos rápido; o BM25 ordena por relevância considerando raridade do termo e tamanho do documento.
  :::
- **P:** "Qual a diferença entre achar e ranquear resultados de busca?"
  :::{dropdown} Resposta modelo
  Achar é recuperar os documentos que contêm os termos — trabalho do índice invertido, rápido e sem scan. Ranquear é ordená-los por relevância — trabalho do TF-IDF/BM25, que pondera frequência do termo no documento, raridade no acervo, saturação e tamanho do texto. Uma busca boa precisa das duas: recuperar certo e ordenar pelo que mais importa.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 3, índices de busca full-text).
- **Documentação do Elasticsearch/OpenSearch** (análise de texto e BM25) e do **MongoDB Atlas Search**.
- **PostgreSQL — Full Text Search** (tsvector + GIN).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — índices invertidos/full-text. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — armazenamentos de busca. <!-- @reis2022 -->
- Tanimura, C. *SQL for Data Analysis* (2021) — texto e consultas. <!-- @tanimura2021 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
