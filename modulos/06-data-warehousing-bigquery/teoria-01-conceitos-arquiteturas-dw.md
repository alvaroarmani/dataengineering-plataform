# O que é um Data Warehouse: conceitos e arquiteturas (Inmon vs Kimball)

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você já sabe modelar um star schema. Mas onde ele "mora"? Um **Data Warehouse (DW)** é o
banco analítico central de uma empresa — o lugar que reúne dados de várias fontes, limpos e
organizados para **análise e decisão**, separado dos bancos que rodam a operação. Entender o
que é um DW, como ele se organiza em **camadas** e as duas grandes filosofias de projeto
(**Inmon** e **Kimball**) é o que te permite desenhar o seu — inclusive o do TCC.

## 💡 Conceito (o porquê)

### DW = banco para analisar, não para operar (OLAP vs OLTP)
Um sistema **OLTP** (transacional) é otimizado para **muitas escritas pequenas e rápidas**
(gravar um pedido). Um DW é **OLAP** (analítico): poucas escritas, **muitas leituras que
varrem milhões de linhas** para agregar. São cargas de trabalho opostas — por isso separamos:
rodar relatórios pesados direto no banco de produção degrada a operação.

Bill Inmon definiu o DW clássico como uma coleção de dados **orientada a assunto, integrada,
não-volátil e histórica (variável no tempo)** — quatro propriedades que ainda descrevem bem o
que um DW faz.

### Arquitetura em camadas
Dados quase nunca vão da fonte direto para a análise. Passam por camadas:

- **Staging / Raw:** cópia crua dos dados da fonte, como chegaram (aterrissagem).
- **Core / Integrado:** dados limpos, padronizados e integrados de várias fontes — a "fonte
  da verdade".
- **Marts / Consumo:** recortes por área de negócio, geralmente em **star schema**, prontos
  para BI.

```{mermaid}
flowchart LR
    F[(Fontes)] --> S[Staging / Raw] --> C[Core / Integrado] --> M[Marts / Consumo]
    M --> BI[BI e análise]
```

No mundo do **lakehouse** essa mesma ideia reaparece com outros nomes: **bronze → prata →
ouro** (medallion). O princípio é o mesmo: cru → limpo → pronto para consumo.

### Inmon vs Kimball: as duas filosofias
As duas escolas concordam no objetivo, mas discordam no caminho:

| | **Inmon (top-down)** | **Kimball (bottom-up)** |
|---|---|---|
| Ideia central | Um **EDW corporativo normalizado** primeiro; marts derivam dele | **Marts dimensionais** por processo, integrados por dimensões conformadas |
| Modelagem do core | Normalizada (3FN) | Dimensional (star) |
| Começo | Amplo (empresa toda) | Incremental (um processo por vez) |
| Entrega de valor | Mais lenta no início, consistente no fim | Rápida por área, integra via **bus architecture** |

Na prática, muitos DWs são **híbridos**: um core mais normalizado/integrado alimentando marts
dimensionais (Kimball) para consumo — juntando o melhor dos dois. O importante é entender o
**trade-off**, não torcer por um "time".

### Dimensões conformadas (o segredo da integração no Kimball)
Uma **dimensão conformada** é compartilhada entre vários fatos/marts (a mesma `dim_cliente`
serve vendas e devoluções). É o que impede "ilhas de dados" no approach bottom-up — a
**bus architecture** de Kimball.

## 🔎 Exemplo
Num e-commerce: os CSVs do Olist chegam ao **staging** como estão; um passo de limpeza
integra e padroniza no **core** (clientes deduplicados, categorias traduzidas); e um **mart**
dimensional (o star `fato_item_pedido` + dims) serve os dashboards de vendas. Se amanhã
surgir um mart de **devoluções**, ele reaproveita a **mesma `dim_cliente` e `dim_produto`**
(conformadas) — os números batem entre os dois.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley resumem o debate: a abordagem **top-down de Inmon** constrói um Enterprise Data
Warehouse normalizado como fonte única antes dos marts; a **bottom-up de Kimball** entrega
marts dimensionais por processo, integrados por dimensões conformadas. Hoje as fronteiras se
misturam, e a escolha é de trade-off, não de dogma. — *Fundamentals of Data Engineering*, cap. 8.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Kleppmann observa que empresas separam um banco OLTP de produção de um DW OLAP justamente
porque as cargas são antagônicas, e que o esquema estrela domina os DWs analíticos porque
casa com o padrão de consulta "varrer o fato e juntar dimensões". — *Designing Data-Intensive
Applications*, cap. 3.
:::

## ⚠️ Erros comuns
- **Rodar análise no banco de produção** (OLTP) — degrada a operação; é para isso que existe o DW.
- Tratar Inmon vs Kimball como religião — o trade-off é situacional, e híbridos são comuns.
- Pular a camada **core** e ligar marts direto no staging cru — replica limpeza e diverge números.
- Marts que **não compartilham dimensões conformadas** — viram ilhas com números que não batem.
- Confundir **DW** (modelado, para consumo) com **data lake** (arquivos crus) — são camadas diferentes.

## 💼 O que o mercado espera
Saber explicar OLTP vs OLAP, a arquitetura em camadas e o contraste Inmon/Kimball é assunto
de entrevista de Data/Analytics Engineer. Times reais falam em "camadas" (staging/core/marts
ou bronze/prata/ouro) o tempo todo — é o vocabulário do dia a dia.

:::{admonition} ✨ Em resumo
:class: resumo
- **DW** = banco analítico (OLAP) central: orientado a assunto, integrado, não-volátil, histórico.
- Dados fluem em **camadas**: staging/raw → core/integrado → marts/consumo (eco do bronze→prata→ouro).
- **Inmon** = top-down, core normalizado primeiro; **Kimball** = bottom-up, marts dimensionais
  integrados por **dimensões conformadas**. Híbridos são comuns.
- Nunca analise no OLTP de produção; nunca deixe marts virarem ilhas sem dimensões conformadas.
:::

## 🧠 Quiz de recall
1. Qual a diferença entre OLTP e OLAP?
   :::{dropdown} Resposta
   OLTP é transacional (muitas escritas pequenas e rápidas, roda a operação); OLAP é analítico (muitas leituras que varrem/agregam grandes volumes). Cargas opostas, por isso separamos o DW do banco de produção.
   :::
2. Quais as camadas típicas de um DW e o papel de cada uma?
   :::{dropdown} Resposta
   Staging/raw (cópia crua da fonte), core/integrado (limpo, padronizado, fonte da verdade) e marts/consumo (recortes dimensionais para BI). No lakehouse: bronze/prata/ouro.
   :::
3. Resuma Inmon vs Kimball.
   :::{dropdown} Resposta
   Inmon: top-down, EDW normalizado primeiro, marts derivam dele. Kimball: bottom-up, marts dimensionais por processo integrados por dimensões conformadas (bus architecture). Muitos DWs são híbridos.
   :::
4. O que é uma dimensão conformada e por que importa?
   :::{dropdown} Resposta
   Uma dimensão compartilhada entre vários fatos/marts (mesma dim_cliente em vendas e devoluções). Garante que os números batam entre áreas e evita ilhas de dados.
   :::
5. Cite as quatro propriedades do DW segundo Inmon.
   :::{dropdown} Resposta
   Orientado a assunto, integrado, não-volátil e variável no tempo (histórico).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que não rodar os relatórios direto no banco de produção?"
  :::{dropdown} Resposta modelo
  Porque OLTP e OLAP têm cargas antagônicas: consultas analíticas varrem muitas linhas e competem por recursos com as transações, degradando a operação. O DW isola a análise, com modelagem e armazenamento (colunar) otimizados para leitura.
  :::
- **P:** "Você usaria Inmon ou Kimball num projeto novo?"
  :::{dropdown} Resposta modelo
  Depende do contexto. Kimball entrega valor rápido por processo e integra via dimensões conformadas — ótimo para começar e mostrar resultado. Inmon dá uma base corporativa consistente, útil em ambientes muito integrados. Na prática costumo ir híbrido: um core integrado alimentando marts dimensionais para consumo.
  :::
- **P:** "O que diferencia um data warehouse de um data lake?"
  :::{dropdown} Resposta modelo
  O data lake guarda dados crus (arquivos, vários formatos) barato e flexível; o DW guarda dados modelados e limpos, otimizados para consulta analítica. O lakehouse tenta unir os dois, com camadas (bronze/prata/ouro) sobre armazenamento de objetos.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering**, cap. 8 (arquiteturas de DW, Inmon vs Kimball).
- **Kleppmann — Designing Data-Intensive Applications**, cap. 3 (data warehousing, OLTP vs OLAP).
- **Kimball & Ross — The Data Warehouse Toolkit** (bus architecture, dimensões conformadas).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 8 (arquiteturas de DW). <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 3 (data warehousing; OLTP vs OLAP). <!-- @kleppmann2017 -->
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit*, 3ª ed. (2013) — bus architecture, dimensões conformadas. <!-- @kimball2013 -->
- Inmon, W. H. *Building the Data Warehouse*, 4ª ed. (2005) — abordagem top-down (EDW normalizado). <!-- @inmon2005 -->

*Acessado em: 2026-08-23.*

---
**Revisado em:** 2026-08-23
