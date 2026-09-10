# Modelagem dimensional avançada: tipos de fato, dimensões e o bus matrix

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você já sabe o básico: fato no centro, dimensões ao redor, grão definido, SCD2 para histórico
(teorias 01–04). Mas o mundo real quebra o "star schema de manual" o tempo todo: como medir o
**tempo entre etapas** de um pedido (criado → pago → enviado → entregue)? Como ligar um paciente a
**vários** diagnósticos (muitos-para-muitos)? Como saber que "cliente" no time de vendas é o **mesmo**
"cliente" do marketing, para cruzar os dois? Como registrar que **algo não aconteceu** (um carrinho
sem compra)? Responder a isso é o que separa quem "desenha um star schema" de quem **arquiteta um
data warehouse corporativo** — o nível que uma pós cobra. Esta unidade reúne os padrões avançados de
Kimball que resolvem esses casos.

## 💡 Conceito (o porquê)

### Os quatro tipos de tabela fato
Nem toda fato é igual. Escolher o tipo certo é uma decisão de arquitetura:

- **Transaction fact (transacional):** uma linha por **evento** (uma venda, um clique). O tipo mais
  comum; grão fino, aditivo. "Quanto vendemos?" → soma linhas.
- **Periodic snapshot (foto periódica):** uma linha por **entidade por período** (saldo de cada conta
  **no fim de cada dia**). Ótimo para métricas de estoque/saldo que só fazem sentido "no instante X".
  Medidas são **semi-aditivas** (você soma saldos entre contas, mas **não** entre dias — soma de
  saldos diários não é nada).
- **Accumulating snapshot (foto acumulada):** uma linha por **item que percorre um pipeline com
  marcos**, com **uma coluna de data por etapa** (criado, pago, enviado, entregue) que vai sendo
  **preenchida (UPDATE)** conforme o item avança. Permite medir **durações entre marcos** (lead time)
  — o coração de análises de processo/funil.
- **Factless fact (fato sem medida):** uma linha que registra que um **evento/relação ocorreu**, sem
  medida numérica. Serve para contar ocorrências ("quantos alunos se matricularam em cada curso?") e,
  crucialmente, para analisar o que **não** aconteceu (cobertura: cursos sem matrícula) via um
  left-join contra o que era possível.

### Aditividade das medidas (a pegadinha silenciosa)
Uma medida pode ser **aditiva** (some em qualquer dimensão — receita), **semi-aditiva** (some em
algumas, não no tempo — saldo, estoque) ou **não-aditiva** (nunca some diretamente — percentuais,
razões, temperaturas). Somar uma medida semi/não-aditiva na dimensão errada é um dos erros mais
comuns e **silenciosos** de BI. O tipo de fato e a aditividade andam juntos.

### Padrões avançados de dimensão
O star schema real usa mais que dimensões simples:
- **Role-playing:** a mesma dimensão (`dim_data`) exercendo **papéis** diferentes na fato (data do
  pedido, data do envio, data da entrega) — via views/aliases, sem duplicar a tabela.
- **Degenerate dimension:** um atributo "dimensional" que vive **na própria fato** por não ter mais
  nada a descrever — tipicamente o **número da nota/pedido** (identificador de transação).
- **Junk dimension:** juntar várias **flags/booleanos** soltos (é_presente?, é_promoção?) numa única
  dimensão de combinações, em vez de poluir a fato com dezenas de colunas.
- **Bridge table (ponte):** resolve **muitos-para-muitos** entre fato e dimensão (um pedido com vários
  cupons; um paciente com vários diagnósticos). A ponte liga a fato a um **grupo**, com um peso de
  alocação quando preciso — evita explodir o grão.
- **Mini-dimension / outrigger:** separar atributos que mudam muito rápido (faixa de renda) numa
  mini-dimensão (parente do SCD tipo 4), para não estourar o SCD2 da dimensão principal.

### Dimensões conformadas e o Bus Matrix
O salto de "um star schema" para "um **data warehouse corporativo**": **dimensões conformadas** são
dimensões **compartilhadas e idênticas** entre vários processos de negócio (a mesma `dim_cliente`
serve vendas, suporte e marketing). Elas permitem **drill-across** — cruzar métricas de processos
diferentes pela dimensão comum ("receita × chamados de suporte por cliente"). O **Bus Matrix** de
Kimball é o mapa disso: linhas = processos de negócio (vendas, estoque, entregas), colunas =
dimensões conformadas; cada X marca quais dimensões cada processo usa. É a **arquitetura** que mantém
o DW coerente e integrável, em vez de silos de star schemas isolados.

```mermaid
flowchart TB
    subgraph Dimensões conformadas (compartilhadas)
      D1[dim_data]:::d
      D2[dim_cliente]:::d
      D3[dim_produto]:::d
    end
    F1[fato_vendas]:::f --> D1 & D2 & D3
    F2[fato_estoque<br/>periodic snapshot]:::f --> D1 & D3
    F3[fato_entregas<br/>accumulating snapshot]:::f --> D1 & D2
    classDef d fill:#1f8a4c,color:#fff;
    classDef f fill:#0b5cad,color:#fff;
```
*Três processos (vendas, estoque, entregas), cada um com o tipo de fato adequado, unidos pelas mesmas
dimensões conformadas — o Bus Matrix na prática.*

### SCD além do 2: tipos 4 e 6
A teoria 03 cobriu SCD 1 (sobrescreve), 2 (versiona) e 3 (coluna "valor anterior"). Em escala:
- **Tipo 4 (mini-dimension):** atributos voláteis saem para uma dimensão separada, evitando gerar
  milhões de versões SCD2 na dimensão principal.
- **Tipo 6 (híbrido 1+2+3):** combina versão histórica (2) com um atributo "valor atual" sempre
  sobrescrito (1/3) na mesma linha — permite analisar tanto "como era na época" quanto "como é hoje".

### Armadilhas de grão: fan trap e chasm trap
Juntar tabelas de grãos diferentes num só join **duplica linhas** e **infla medidas** (o *fan trap*:
somar receita depois de juntar com uma tabela 1-para-muitos conta cada venda várias vezes). O
*chasm trap* é o oposto: dois muitos-para-um a partir de um centro produzem um produto cartesiano.
A defesa é **respeitar o grão** — agregar cada fato no seu grão antes de cruzar, ou usar bridge
tables — nunca juntar fatos de grãos diferentes cruamente.

## 🔎 Exemplo
Uma logística modela três processos num só DW. **Vendas** é uma *transaction fact* (uma linha por
item). **Estoque** é um *periodic snapshot* (saldo por produto ao fim de cada dia; medida
semi-aditiva — nunca some estoques de dias diferentes). **Entregas** é um *accumulating snapshot*:
uma linha por pedido com datas de `criado/pago/enviado/entregue` que vão sendo preenchidas, medindo
o **lead time** de cada etapa. Os três compartilham `dim_data`, `dim_produto` e `dim_cliente`
**conformadas**, então o time cruza "receita × giro de estoque × tempo de entrega" por produto —
drill-across pelo Bus Matrix. Um pedido com vários cupons usa uma **bridge table**; o número do
pedido é uma **degenerate dimension** na fato. É um DW corporativo, não um star schema solto.

:::{admonition} 📖 Da literatura
:class: seealso
Kimball & Ross detalham os **três tipos de fato** (transaction, periodic e accumulating snapshot),
os fatos **factless**, os padrões de dimensão (role-playing, junk, degenerate, bridge, mini-dimension)
e, como espinha da arquitetura, as **dimensões conformadas** e o **Enterprise Data Warehouse Bus
Matrix**. — *The Data Warehouse Toolkit* (caps. de técnicas dimensionais e bus architecture).
:::

:::{admonition} 🏭 Do mundo real
:class: important
O que distingue um DW corporativo de um amontoado de star schemas é a **conformidade das dimensões**:
sem uma `dim_cliente` única e compartilhada, "cliente" significa coisas diferentes em cada área e
nada cruza. Por isso times maduros começam pelo **Bus Matrix** (quais processos × quais dimensões)
antes de modelar tabela por tabela — é a decisão de arquitetura que evita silos. — Kimball & Ross.
:::

## ⚠️ Erros comuns
- **Somar medida semi-aditiva no tempo** (saldos/estoques entre dias) — número sem sentido.
- **Usar transaction fact para tudo** — perde-se lead time (accumulating) e fotos de saldo (periodic).
- **Explodir o grão** para modelar muitos-para-muitos em vez de usar **bridge table**.
- **Dimensões não conformadas** — cada área com sua "dim_cliente"; nada cruza (silos).
- **Fan/chasm trap** — juntar fatos de grãos diferentes crua e inflar medidas.
- **Ignorar o factless fact** — não conseguir analisar o que **não** aconteceu (cobertura).

## 💼 O que o mercado espera
No nível pleno/sênior, espera-se escolher o **tipo de fato** certo, reconhecer aditividade, aplicar
dimensões avançadas (role-playing, junk, degenerate, bridge), e — o divisor de águas — projetar
**dimensões conformadas / Bus Matrix** para um DW integrado. Cases de modelagem em entrevista quase
sempre escondem um desses padrões (um many-to-many, um lead time, uma medida semi-aditiva).

:::{admonition} ✨ Em resumo
:class: resumo
- **Tipos de fato**: transaction (evento), **periodic snapshot** (saldo por período, semi-aditivo), **accumulating snapshot** (pipeline com marcos, lead time), **factless** (ocorrência/cobertura).
- **Aditividade** (aditiva/semi/não) dita onde a medida pode ser somada — somar errado é bug silencioso.
- **Dimensões avançadas**: role-playing, degenerate, junk, **bridge (M:N)**, mini-dimension.
- **Dimensões conformadas + Bus Matrix** transformam star schemas soltos num **DW corporativo** integrável (drill-across). SCD **4** (mini-dim) e **6** (híbrido) além do 2.
:::

## 🧠 Quiz de recall
1. Quais são os quatro tipos de tabela fato e para que servem?
   :::{dropdown} Resposta
   Transaction (uma linha por evento), periodic snapshot (saldo por entidade por período), accumulating snapshot (item num pipeline com marcos, para lead time) e factless (registra ocorrência/relação, sem medida — conta e analisa cobertura).
   :::
2. O que é uma medida semi-aditiva? Dê um exemplo do erro.
   :::{dropdown} Resposta
   Uma medida que soma em algumas dimensões mas não no tempo (ex.: saldo, estoque). Erro clássico: somar saldos de dias diferentes — o resultado não significa nada.
   :::
3. Para que serve uma bridge table?
   :::{dropdown} Resposta
   Resolver relacionamentos muitos-para-muitos entre fato e dimensão (pedido com vários cupons; paciente com vários diagnósticos) sem explodir o grão da fato, ligando a fato a um grupo (com peso de alocação se necessário).
   :::
4. O que são dimensões conformadas e por que são a base de um DW corporativo?
   :::{dropdown} Resposta
   Dimensões compartilhadas e idênticas entre vários processos (a mesma dim_cliente em vendas, suporte, marketing). Permitem drill-across (cruzar métricas de processos diferentes) e evitam silos; o Bus Matrix mapeia processos × dimensões.
   :::
5. O que é o fan trap?
   :::{dropdown} Resposta
   Juntar tabelas de grãos diferentes (1-para-muitos) e depois somar uma medida, contando-a várias vezes e inflando o resultado. Defesa: respeitar o grão (agregar antes de cruzar) ou usar bridge tables.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você mediria o tempo médio entre o pedido e a entrega, por transportadora?"
  :::{dropdown} Resposta modelo
  Com um accumulating snapshot fact de entregas: uma linha por pedido com colunas de data por marco (criado, pago, enviado, entregue), preenchidas via UPDATE conforme o pedido avança. As durações entre marcos (lead times) são medidas derivadas dessas datas. Junto a uma dim_transportadora conformada, agrego a média por transportadora. Transaction fact não serviria bem — ela registra eventos, não o ciclo de vida do item.
  :::
- **P:** "Vendas e suporte têm cada um sua tabela de cliente. Como integrar para cruzar receita e chamados?"
  :::{dropdown} Resposta modelo
  Conformando a dimensão: uma única dim_cliente compartilhada (mesma chave, mesmos atributos) por ambos os processos. Aí faço drill-across — agrego receita na fato de vendas e chamados na fato de suporte, cada uma no seu grão, e junto pelos atributos da dim_cliente conformada. Sem conformidade, "cliente" diverge e nada cruza; por isso eu partiria de um Bus Matrix definindo quais dimensões são conformadas entre os processos.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kimball & Ross — The Data Warehouse Toolkit** (tipos de fato, dimensões avançadas, Bus Matrix).
- **Reis & Housley — Fundamentals of Data Engineering** (modelagem no ciclo de vida).
- **Inmon — Building the Data Warehouse** (a visão corporativa/top-down como contraponto).

## 📚 Referências
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit* (2013) — tipos de fato, dimensões, Bus Matrix. <!-- @kimball2013 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — modelagem dimensional. <!-- @reis2022 -->
- Inmon, W. *Building the Data Warehouse* (2005) — arquitetura corporativa de DW. <!-- @inmon2005 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
