# Surrogate keys: chaves substitutas nas dimensões

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

No sistema transacional, cada produto já tem um identificador: o SKU, o CPF do cliente, o
código do pedido. É tentador usar **essa mesma chave natural** como chave da dimensão no
Data Warehouse. Parece prático — até o dia em que o SKU é reaproveitado para outro produto,
o sistema de origem muda o formato do código, ou você precisa **guardar duas versões** do
mesmo cliente (o endereço mudou). Aí a chave natural falha. A solução do padrão Kimball é
simples e poderosa: dar a cada linha da dimensão uma **chave própria, artificial e sem
significado de negócio** — a *surrogate key*.

## 💡 Conceito (o porquê)

### Chave natural vs surrogate key
- **Chave natural** (*natural/business key*): o identificador que vem do sistema de origem —
  SKU do produto, CPF, e-mail, código do pedido. Tem **significado de negócio**.
- **Surrogate key** (*chave substituta*): um inteiro **sequencial, gerado pelo DW**, sem
  significado nenhum além de identificar aquela linha da dimensão. Ex.: `sk_produto = 1, 2, 3…`.

A tabela fato passa a referenciar a **surrogate key** da dimensão, não a chave natural. A
dimensão guarda **as duas**: a surrogate (sua chave primária) e a natural (para reconciliar
com a origem).

### Por que usar surrogate keys
1. **Isolamento da origem:** se o sistema fonte muda o formato do código (ou troca de sistema),
   o DW não precisa reescrever a fato inteira — só o mapeamento na dimensão.
2. **Histórico (SCD Tipo 2):** para versionar uma dimensão que muda no tempo, você precisa de
   **várias linhas com a mesma chave natural** — só a surrogate key as distingue. É o que
   habilita o histórico (assunto da próxima unidade).
3. **Integração de múltiplas fontes:** dois sistemas podem ter o cliente "123" significando
   pessoas diferentes; a surrogate unifica sob uma chave única do DW.
4. **Performance e espaço:** um `INTEGER` como chave é mais rápido para JOIN e ocupa menos que
   uma string longa (CPF, e-mail) repetida em milhões de linhas do fato.
5. **Chaves reaproveitadas/nulas:** se a origem reaproveita códigos ou tem registros sem chave,
   a surrogate dá uma identidade estável mesmo assim.

### Como gerar a surrogate key
- **Sequência do banco** (`SERIAL`/`IDENTITY`/`AUTO_INCREMENT`) — o jeito clássico em Postgres.
- **`ROW_NUMBER()`** ao carregar a dimensão a partir de uma *staging* — comum em SQL analítico.
- **No dbt** (M07), pacotes geram surrogate keys por hash das chaves naturais.

### Como a fato recebe a surrogate key (surrogate key lookup)
Ao carregar o fato, os dados chegam com a **chave natural** (o SKU da venda). O ETL faz um
**JOIN com a dimensão pela chave natural** para trocar o SKU pela **surrogate key** — esse
passo se chama *surrogate key lookup* e é o coração do carregamento de fatos.

## 🔎 Exemplo

Staging de produtos vindo da origem, com o código de negócio:

| codigo | categoria |
|--------|-----------|
| P-100  | eletronicos |
| P-050  | livros |

Vira a dimensão com surrogate key:

| sk_produto | codigo (natural) | categoria |
|------------|------------------|-----------|
| 1 | P-050 | livros |
| 2 | P-100 | eletronicos |

Uma venda chega como `(venda_id=9, codigo_produto='P-100', valor=1500)`. O *lookup* junta com
`dim_produto` por `codigo` e grava no fato `sk_produto = 2` — a fato nunca guarda 'P-100'.

:::{admonition} 📖 Da literatura
:class: seealso
Kimball é enfático: **toda tabela de dimensão deve ter uma surrogate key** como chave
primária — um inteiro sem significado, atribuído pelo DW — e as tabelas fato devem usar
essas surrogate keys em vez das chaves naturais da origem. É o que ele chama de uma das
regras não-negociáveis da modelagem dimensional. — *The Data Warehouse Toolkit*, cap. 2.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Kleppmann observa que identificadores com significado de negócio tendem a "vazar" premissas
que mudam com o tempo (formatos, faixas, reuso), enquanto um identificador artificial e
estável desacopla o modelo de dados dessas mudanças — a mesma lógica que sustenta as
surrogate keys no DW. — *Designing Data-Intensive Applications*, cap. 3.
:::

## ⚠️ Erros comuns
- **Usar a chave natural como PK da dimensão** — quebra quando a origem reaproveita/muda o código e impossibilita o SCD2.
- **Jogar fora a chave natural** — sem ela você não reconcilia com a origem nem faz o *lookup*.
- **Fazer o fato referenciar a chave natural** — perde os benefícios (performance, histórico, integração).
- **Reaproveitar uma surrogate key** ao recarregar a dimensão — ela deve ser estável ao longo do tempo.
- Dar significado à surrogate (ex.: embutir a data nela) — ela deve ser **opaca**.

## 💼 O que o mercado espera
Explicar **por que** um DW usa surrogate keys (e não o CPF/SKU) é pergunta clássica de
entrevista de Analytics/Data Engineer. Na prática, você vai gerar surrogate keys em dbt e
escrever o *surrogate key lookup* ao carregar fatos — é rotina no dia a dia.

:::{admonition} ✨ Em resumo
:class: resumo
- **Surrogate key** = inteiro artificial, sequencial, sem significado, gerado pelo DW; é a PK da dimensão.
- A dimensão guarda **surrogate + chave natural**; o **fato referencia a surrogate**.
- Vantagens: isola da origem, habilita **histórico (SCD2)**, integra fontes, é rápida/compacta.
- Carregar fato = **surrogate key lookup**: JOIN pela chave natural para trocar pelo `sk`.
:::

## 🧠 Quiz de recall
1. O que é uma surrogate key e como ela difere de uma chave natural?
   :::{dropdown} Resposta
   Surrogate key é um inteiro artificial, sequencial e sem significado de negócio, gerado pelo DW, usado como PK da dimensão. A chave natural (SKU, CPF) vem da origem e tem significado de negócio.
   :::
2. Por que a tabela fato deve referenciar a surrogate key, não a natural?
   :::{dropdown} Resposta
   Para isolar o DW de mudanças na origem, ganhar performance/espaço (inteiro vs string), integrar múltiplas fontes e permitir histórico (SCD2). A fato nunca guarda o código de negócio.
   :::
3. A dimensão deve guardar a chave natural também? Por quê?
   :::{dropdown} Resposta
   Sim. Ela é necessária para reconciliar com o sistema de origem e para o *surrogate key lookup* (encontrar o `sk` a partir do código natural ao carregar o fato).
   :::
4. O que é o "surrogate key lookup" no carregamento de fatos?
   :::{dropdown} Resposta
   É o passo em que o ETL junta os dados que chegam (com a chave natural) à dimensão pela chave natural para substituí-la pela surrogate key antes de gravar o fato.
   :::
5. Por que surrogate keys são pré-requisito para SCD Tipo 2?
   :::{dropdown} Resposta
   Porque no SCD2 a mesma entidade (mesma chave natural) tem várias linhas/versões na dimensão; só a surrogate key (única por linha) consegue distinguir cada versão.
   :::
6. Cite duas formas de gerar surrogate keys.
   :::{dropdown} Resposta
   Sequência/IDENTITY do banco (SERIAL no Postgres) e `ROW_NUMBER()` ao carregar de uma staging; no dbt, também por hash das chaves naturais.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que não usar o CPF do cliente como chave da dimensão?"
  :::{dropdown} Resposta modelo
  Porque a chave natural carrega premissas de negócio que mudam (formato, reuso, nulos), acopla o DW à origem e impede versionar o cliente no tempo (SCD2). Uma surrogate key opaca e estável desacopla o modelo, é mais rápida em JOINs e mantém a chave natural como atributo para reconciliação.
  :::
- **P:** "Como você carrega uma tabela fato garantindo as chaves corretas?"
  :::{dropdown} Resposta modelo
  Os dados chegam com as chaves naturais; para cada dimensão faço o *surrogate key lookup* — JOIN com a dimensão pela chave natural para obter a surrogate key — e gravo no fato apenas as surrogate keys e as métricas, no grão declarado.
  :::
- **P:** "Onde a surrogate key é gerada e como garantir que ela não se repita?"
  :::{dropdown} Resposta modelo
  É gerada pelo DW ao carregar a dimensão (sequência/IDENTITY, `ROW_NUMBER()` ou hash no dbt). Garante-se unicidade tratando a dimensão como *append/upsert* controlado: novas linhas ganham novos valores e valores existentes nunca são reatribuídos, mantendo as referências do fato estáveis.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kimball & Ross — The Data Warehouse Toolkit**, cap. 2 (surrogate keys como regra da dimensão).
- **Reis & Housley — Fundamentals of Data Engineering**, cap. 8 (modelagem para consumo e chaves).

## 📚 Referências
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit*, 3ª ed. (2013) — cap. 2 (surrogate keys). <!-- @kimball2013 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 3 (identificadores estáveis vs de negócio). <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 8 (modelagem e chaves). <!-- @reis2022 -->

*Acessado em: 2026-08-23.*

---
**Revisado em:** 2026-08-23
