# Modelando a partir de um processo de negócio (case Olist)

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você aprendeu as peças — fatos, dimensões, grão, surrogate keys, SCDs. Agora falta o que
mais importa numa entrevista e no TCC: **partir de um negócio real e chegar a um star schema**.
Vamos fazer isso com o **Olist**, um dataset público de e-commerce brasileiro (pedidos,
itens, produtos, clientes, pagamentos). É o mesmo caminho que você repetirá no seu Data
Warehouse final.

## 💡 Conceito (o porquê)

Kimball propõe **quatro passos**, sempre nesta ordem:

### Passo 1 — Escolher o processo de negócio
Um processo é uma **atividade que gera eventos mensuráveis**: vendas, pagamentos, envios,
avaliações. No Olist, o processo central é a **venda** (mais precisamente, os **itens
vendidos** em cada pedido). Escolha o processo que responde às perguntas de negócio mais
importantes — aqui, "quanto vendemos, de quê, para quem, quando".

### Passo 2 — Declarar o grão
A decisão nº 1. No Olist, um pedido pode ter **vários itens** (produtos diferentes, cada um
com preço e frete). O grão mais útil é **uma linha por item de pedido** (`order_item`) — o
mais fino disponível. Com esse grão você ainda consegue "subir" para o nível de pedido
somando; o contrário (descer de pedido para item) seria impossível. **Grão fino = mais
flexível.**

### Passo 3 — Identificar as dimensões
As dimensões são o **contexto** ("por quem/o quê/quando/onde") do item vendido:

- **`dim_cliente`** — quem comprou (cidade, estado). Candidata a **SCD2** se o endereço mudar.
- **`dim_produto`** — o que foi vendido (categoria). Note que o Olist traz a categoria em
  português; a tradução para inglês é um passo de limpeza típico.
- **`dim_data`** — quando (dia, mês, ano) — quase toda análise é temporal.
- **`dim_vendedor`** — quem vendeu (opcional, para marketplace).

Cada dimensão ganha uma **surrogate key** (unidade 2).

### Passo 4 — Identificar os fatos (métricas)
As métricas numéricas do item vendido, consistentes com o grão:

- **`price`** (preço do item) e **`freight_value`** (frete). Ambas são **aditivas** — podem
  ser somadas em qualquer dimensão, o tipo de métrica mais fácil de usar.

### O resultado: o star schema do Olist

```{mermaid}
flowchart TB
    DC[dim_cliente] --> F[fato_item_pedido<br/>grão: 1 item de pedido<br/>price, freight_value]
    DP[dim_produto] --> F
    DD[dim_data] --> F
    DV[dim_vendedor] --> F
```

Do modelo transacional normalizado do Olist (várias tabelas ligadas por IDs) chegamos a um
star: uma fato no grão do item + dimensões descritivas com surrogate keys. Consultar vira
"junte a fato com as dimensões que interessam e agregue".

## 🔎 Exemplo

Pergunta de negócio: **"receita por categoria de produto por estado do cliente"**. Com o star:
junte `fato_item_pedido` a `dim_produto` (categoria) e `dim_cliente` (estado), agrupe por
categoria e estado, some `price`. Sem o star, seriam vários JOINs sobre as tabelas cruas do
Olist e uma query bem mais difícil de ler.

:::{admonition} 📖 Da literatura
:class: seealso
Kimball insiste que a modelagem começa pelo **processo de negócio**, não pelos relatórios que
alguém pediu: modelar o processo (as vendas) gera um star reutilizável para muitas perguntas,
enquanto modelar "o relatório X" produz uma solução frágil e específica. — *The Data
Warehouse Toolkit*, cap. 1–2.
:::

:::{admonition} 🏭 Do mundo real
:class: important
O Olist é um dataset de e-commerce real (marketplace brasileiro) muito usado para praticar
modelagem dimensional — pedidos, itens, produtos, clientes, pagamentos e avaliações. Veja o
catálogo em [`datasets/README.md`](../../datasets/README.md) para baixar e reproduzir. É a
base sugerida para o **TCC** deste curso.
:::

## ⚠️ Erros comuns
- **Grão no nível do pedido** quando existem itens — perde a análise por produto e mistura preços.
- Modelar "o relatório pedido pelo chefe" em vez do **processo** — gera um modelo que só serve para aquela pergunta.
- Esquecer a **dim_data** (quase toda análise do Olist é temporal: sazonalidade, crescimento).
- Deixar a **categoria em português cru** sem padronizar/traduzir — atrapalha joins e leitura.
- Somar métricas **não aditivas** (ex.: uma taxa percentual) como se fossem aditivas.

## 💼 O que o mercado espera
"Modele um e-commerce" é *case* recorrente de entrevista. Saber conduzir os 4 passos em voz
alta — e **justificar o grão** — vale mais que decorar sintaxe. É exatamente o que você
entrega no TCC e no que os times de Analytics Engineering trabalham no dia a dia.

:::{admonition} ✨ Em resumo
:class: resumo
- Modele **o processo de negócio** (a venda), não um relatório específico.
- **Grão fino** (1 item de pedido) = máxima flexibilidade; sempre dá para agregar para cima.
- Dimensões (cliente, produto, data, vendedor) com **surrogate keys**; métricas aditivas
  (`price`, `freight_value`) na fato.
- O star do Olist transforma perguntas de negócio em "junte a fato com as dimensões e agregue".
:::

## 🧠 Quiz de recall
1. Quais são os 4 passos de Kimball, na ordem?
   :::{dropdown} Resposta
   1) Escolher o processo de negócio; 2) declarar o grão; 3) identificar as dimensões; 4) identificar os fatos (métricas).
   :::
2. Por que o grão do Olist deve ser "1 item de pedido" e não "1 pedido"?
   :::{dropdown} Resposta
   Porque um pedido tem vários itens com preço/frete próprios; o grão de item é o mais fino e permite agregar para o nível de pedido — o contrário seria impossível.
   :::
3. Quais dimensões você identificaria para o processo de vendas do Olist?
   :::{dropdown} Resposta
   dim_cliente (cidade/estado), dim_produto (categoria), dim_data (dia/mês/ano) e, opcionalmente, dim_vendedor. Cada uma com surrogate key.
   :::
4. Por que modelar o processo em vez de "o relatório pedido"?
   :::{dropdown} Resposta
   Modelar o processo (vendas) gera um star reutilizável para muitas perguntas; modelar um relatório específico produz uma solução frágil que só serve àquela pergunta.
   :::
5. `price` e `freight_value` são métricas de que tipo, e por que isso importa?
   :::{dropdown} Resposta
   São aditivas — podem ser somadas em qualquer dimensão. Isso as torna simples de usar em qualquer agregação (por categoria, estado, mês).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Modele um star schema para o e-commerce Olist. Comece pelo grão."
  :::{dropdown} Resposta modelo
  Processo: vendas. Grão: um item de pedido (order_item). Fato `fato_item_pedido` com métricas aditivas `price` e `freight_value` e surrogate keys para as dimensões. Dimensões: `dim_cliente` (estado/cidade), `dim_produto` (categoria), `dim_data` e `dim_vendedor`. Perguntas de negócio viram joins da fato com as dimensões desejadas + agregação.
  :::
- **P:** "O cliente do Olist pode mudar de cidade. Como você trata isso?"
  :::{dropdown} Resposta modelo
  Se o negócio precisa do histórico geográfico, `dim_cliente` vira SCD Tipo 2: nova linha por versão, com surrogate key própria e colunas de vigência, para que vendas antigas continuem ligadas ao estado da época.
  :::
- **P:** "Como você escolheria entre grão de item e grão de pedido?"
  :::{dropdown} Resposta modelo
  Escolho o mais fino que os dados permitem — item —, porque preserva o máximo de detalhe (preço/frete por produto) e sempre posso agregar para o nível de pedido. Um grão mais grosso jogaria fora informação irrecuperável.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kimball & Ross — The Data Warehouse Toolkit**, caps. 1–2 (processo → grão → dimensões → fatos).
- **Tanimura — SQL for Data Analysis** (analisando o star com agregações e janelas).
- Catálogo de datasets do curso: [`datasets/README.md`](../../datasets/README.md) (Olist).

## 📚 Referências
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit*, 3ª ed. (2013) — cap. 1–2 (os 4 passos). <!-- @kimball2013 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 8 (modelagem para consumo). <!-- @reis2022 -->
- Tanimura, C. *SQL for Data Analysis* (2021) — análise sobre modelos dimensionais. <!-- @tanimura2021 -->

*Acessado em: 2026-08-23.*

---
**Revisado em:** 2026-08-23
