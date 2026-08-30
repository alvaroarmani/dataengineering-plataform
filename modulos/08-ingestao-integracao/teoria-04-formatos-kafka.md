# Formatos de dados (Parquet, Avro) e introdução a streaming (Kafka)

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Depois de trazer os dados, **em que formato guardá-los**? Salvar tudo como CSV é o erro nº 1 —
lento, sem tipos, sem compressão. E o dado nem sempre chega em lotes: às vezes flui **evento a
evento**, em tempo real. Esta unidade fecha o M8 com os **formatos** que o mercado usa
(Parquet, Avro) e uma introdução a **streaming/Kafka** — o vocabulário para quando "batch" não basta.

## 💡 Conceito (o porquê)

### Por linha vs por coluna (recap do M6)
- **Orientado a linha** (CSV, JSON, Avro): guarda um registro inteiro junto. Bom para
  **escrever/ler um registro por vez** (transacional, streaming).
- **Orientado a coluna** (Parquet, ORC): guarda cada coluna junta. Bom para **análise** (ler
  poucas colunas de muitas linhas), com ótima compressão.

### Os formatos que importam
| Formato | Tipo | Schema | Uso típico |
|---|---|---|---|
| **CSV** | linha, texto | não | interoperar, olho humano; ruim para volume |
| **JSON** | linha, texto | não (semi) | APIs, dados aninhados; verboso |
| **Parquet** | **coluna**, binário | sim (embutido) | **análise/DW** (colunar, comprimido) |
| **Avro** | linha, binário | sim (junto) | **streaming/mensageria**, com evolução de schema |

- **Parquet** é o padrão do analítico: colunar, comprimido, com tipos e estatísticas por bloco
  (o que habilita o *pruning* do M6). Salvar o data lake em Parquet ≫ CSV.
- **Avro** guarda o **schema junto** com os dados e suporta **evolução de schema** (adicionar/
  remover campos sem quebrar consumidores antigos) — por isso é comum em Kafka.

### Schema e evolução
Formatos com **schema** (Parquet, Avro) rejeitam dados fora do tipo e documentam a estrutura.
**Evolução de schema** = mudar o schema ao longo do tempo (novo campo opcional, etc.) sem
quebrar quem lê o dado antigo — essencial em sistemas que vivem anos.

### Batch vs streaming
- **Batch:** processa **lotes** periódicos (o que fizemos até aqui). Simples, ótimo custo.
- **Streaming:** processa **eventos contínuos**, com baixa latência (segundos). Necessário para
  detecção de fraude, dashboards ao vivo, etc.

### Kafka em uma imagem
**Apache Kafka** é um **log distribuído** de mensagens (mensageria/streaming):
- **Produtores** escrevem **mensagens** em **tópicos**; **consumidores** leem.
- Um tópico é dividido em **partições** (paralelismo/ordem por partição).
- Cada mensagem tem um **offset** (posição no log); o consumidor **committa** até onde leu — e
  retoma dali (base de "processar exatamente/ao menos uma vez").

```{mermaid}
flowchart LR
    P[Produtor] --> T[(Tópico / partições)]
    T --> C1[Consumidor A]
    T --> C2[Consumidor B]
```
Kafka **desacopla** quem produz de quem consome, absorve picos e permite vários consumidores do
mesmo fluxo — a espinha de arquiteturas de streaming.

## 🔎 Exemplo
Um app emite um evento "pedido criado" a cada compra. Um **produtor** publica no tópico
`pedidos` (mensagem em **Avro**, com schema). Um **consumidor** de analytics lê, guarda o
**offset** e escreve em **Parquet** no data lake para o DW. Se cair, retoma do último offset
committado — sem perder nem duplicar (com idempotência).

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann contrasta armazenamento por linha e por coluna (Parquet para análise), discute
**evolução de schema** (Avro) como requisito de sistemas duradouros, e descreve **logs de
mensagens** (Kafka) como base do processamento de streams. — *Designing Data-Intensive
Applications*, caps. 3, 4 e 11.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Reis & Housley colocam Parquet como formato de fato dos data lakes/lakehouses (colunar +
compressão + schema) e o streaming (Kafka) como a via para dados de baixa latência — batch e
streaming coexistem na maioria das arquiteturas. — *Fundamentals of Data Engineering*.
:::

## ⚠️ Erros comuns
- **Guardar tudo em CSV** — sem tipos, sem compressão, lento; use **Parquet** no analítico.
- Confundir **linha vs coluna** — Parquet para análise; Avro/linha para streaming/registro a registro.
- Ignorar **evolução de schema** — um campo novo quebra consumidores antigos.
- Achar que **tudo precisa de streaming** — batch resolve a maioria, mais simples e barato.
- Não entender **offset/commit** no Kafka — leva a reprocessar ou perder mensagens.

## 💼 O que o mercado espera
Justificar Parquet vs CSV/JSON e saber quando streaming (Kafka) faz sentido é assunto de
entrevista. Conhecer offsets/tópicos/partições — mesmo sem ser especialista em Kafka — mostra
maturidade de arquitetura.

:::{admonition} ✨ Em resumo
:class: resumo
- **Parquet** (colunar, comprimido, com schema) para **análise/DW**; **Avro** (linha, schema
  junto, evolução) para **streaming**; CSV/JSON para interop.
- **Evolução de schema** mantém consumidores antigos funcionando quando o dado muda.
- **Batch** para lotes periódicos; **streaming** para baixa latência.
- **Kafka** = log distribuído: produtores→tópicos(partições)→consumidores, com **offset/commit**.
:::

## 🧠 Quiz de recall
1. Parquet vs CSV — quando e por quê?
   :::{dropdown} Resposta
   Parquet (colunar, binário, comprimido, com schema) para análise/DW — lê poucas colunas de muitas linhas rápido e barato. CSV (linha, texto, sem tipos) só para interop/olho humano; ruim para volume.
   :::
2. Por que Avro é comum em streaming?
   :::{dropdown} Resposta
   É orientado a linha (registro a registro), binário, guarda o schema junto e suporta evolução de schema — encaixa em mensageria como o Kafka.
   :::
3. O que é evolução de schema e por que importa?
   :::{dropdown} Resposta
   Mudar o schema ao longo do tempo (ex.: novo campo opcional) sem quebrar quem lê o dado antigo — essencial em sistemas que duram anos.
   :::
4. Batch vs streaming?
   :::{dropdown} Resposta
   Batch processa lotes periódicos (simples, barato); streaming processa eventos contínuos com baixa latência (para fraude, dashboards ao vivo). A maioria dos casos é batch.
   :::
5. No Kafka, o que é o offset e o commit?
   :::{dropdown} Resposta
   O offset é a posição da mensagem no log da partição; o consumidor committa até onde leu e retoma dali — base para não perder nem reprocessar mensagens.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que não guardar o data lake todo em CSV?"
  :::{dropdown} Resposta modelo
  CSV não tem tipos nem compressão e lê tudo (orientado a linha/texto) — caro e lento para análise. Parquet é colunar, comprimido e com schema/estatísticas, então lê só as colunas necessárias e habilita pruning — muito mais rápido e barato no DW.
  :::
- **P:** "Quando você usaria Kafka/streaming em vez de batch?"
  :::{dropdown} Resposta modelo
  Quando a latência importa (segundos): detecção de fraude, monitoramento ao vivo, sincronização de sistemas via CDC. Para relatórios diários/horários, batch é mais simples e barato. Muitas arquiteturas usam os dois.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications**, caps. 3 (colunar), 4 (Avro/evolução), 11 (streams/Kafka).
- **Reis & Housley — Fundamentals of Data Engineering** (formatos, streaming).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — caps. 3, 4, 11 (colunar, Avro, streams/Kafka). <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — formatos e streaming. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — formatos e padrões de ingestão. <!-- @densmore2021 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
