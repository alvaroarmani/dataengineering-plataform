# Modelagem dimensional: fatos, dimensões e grão

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Um banco transacional (OLTP) é **normalizado** — ótimo para gravar pedidos rápido, péssimo
para analisar (dezenas de JOINs para uma pergunta simples). Para análise, os dados são
remodelados no formato **dimensional** (Kimball): poucas tabelas, joins óbvios, consultas
rápidas e **compreensíveis pelo negócio**. Modelar bem é o que faz um Data Warehouse ser
usável — e é o coração do seu TCC.

## 💡 Conceito (o porquê)

### Fatos e dimensões
O modelo dimensional divide os dados em dois tipos de tabela:

- **Fato** (*fact*): os **eventos mensuráveis** do negócio — uma venda, um clique, um envio.
  Contém **métricas** numéricas (valor, quantidade) e **chaves** para as dimensões. É a
  tabela **grande** (muitas linhas).
- **Dimensão** (*dimension*): o **contexto** que descreve os fatos — quem, o quê, quando,
  onde. Contém atributos **textuais/descritivos** (nome do cliente, categoria do produto,
  mês). São tabelas **pequenas e largas**.

> Fatos respondem "**quanto/quantos**"; dimensões respondem "**por quê/quem/quando/onde**".

### O grão (grain): a decisão nº 1
O **grão** é o que **uma linha da tabela fato representa**. Definir o grão **antes** de tudo
é a regra de ouro de Kimball. Ex.: "uma linha por **item** de pedido" é um grão mais fino que
"uma linha por **pedido**". Todas as métricas e dimensões precisam ser consistentes com o
grão escolhido — misturar grãos gera números errados.

### Star schema
No **esquema estrela**, a tabela fato fica no centro, ligada diretamente às dimensões (como
os pontos de uma estrela):

```{mermaid}
flowchart TB
    DC[dim_cliente] --> F[fato_vendas]
    DP[dim_produto] --> F
    DD[dim_data] --> F
    DL[dim_local] --> F
```

Consultar é simples: junta o fato com as dimensões que você quer e agrega. É **desnormalizado
de propósito** — repetir "São Paulo" em milhares de linhas de dimensão é um preço barato pela
simplicidade e velocidade.

### Star vs snowflake
No **snowflake**, as dimensões são normalizadas em sub-tabelas (ex.: `dim_produto` → `dim_categoria`).
Economiza espaço, mas adiciona JOINs e complexidade. **Kimball prefere o star** na maioria dos
casos: simplicidade e performance ganham do espaço economizado.

## 🔎 Exemplo

Do pedido "ana comprou 2 livros por R$ 25 em 05/01 em SP", o modelo dimensional guarda:
- **fato_vendas**: `(cliente_id=1, produto_id=7, data_id=20260105, quantidade=2, valor=50)`
- **dim_cliente**: `(1, 'ana', 'São Paulo')` · **dim_produto**: `(7, 'livro X', 'livros')` · **dim_data**: `(20260105, '2026-01-05', 2026, 1)`

A pergunta "receita de livros por mês" vira: junte fato + dim_produto + dim_data, filtre
categoria, agrupe por mês, some o valor.

:::{admonition} 📖 Da literatura
:class: seealso
Kimball resume o processo em quatro passos: (1) escolher o **processo de negócio**, (2)
declarar o **grão**, (3) identificar as **dimensões**, (4) identificar os **fatos** (métricas).
Declarar o grão primeiro é inegociável. — *The Data Warehouse Toolkit*, cap. 1–2.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Reis & Housley observam que, mesmo na era do "lakehouse", a modelagem dimensional de Kimball
continua sendo o padrão dominante para as camadas de consumo (marts) — porque é a forma que
analistas e ferramentas de BI entendem melhor. — *Fundamentals of Data Engineering*, cap. 8.
:::

## ⚠️ Erros comuns
- **Não declarar o grão** (ou misturar grãos na mesma fato) → agregações erradas/duplicadas.
- Colocar **métrica** numa dimensão ou **atributo descritivo** no fato.
- Normalizar demais ("snowflake" por reflexo) e encher a análise de JOINs.
- Fato "largo" com textos longos (isso é papel da dimensão).
- Esquecer a **dim_data** — quase toda análise é por tempo.

## 💼 O que o mercado espera
Saber desenhar um star schema e **justificar o grão** é requisito em vagas de Analytics
Engineer/Data Engineer, e cai como *case* em entrevistas ("modele um e-commerce"). É a base
para o dbt (M07) e para o TCC.

:::{admonition} ✨ Em resumo
:class: resumo
- **Fato** = eventos + métricas (grande); **dimensão** = contexto descritivo (pequena/larga).
- **Grão** = o que uma linha do fato representa — **declare primeiro**, seja consistente.
- **Star schema**: fato central + dimensões diretas; desnormalizado de propósito (simples e rápido).
- Star costuma vencer snowflake (menos JOINs); nunca esqueça a **dim_data**.
:::

## 🧠 Quiz de recall
1. Qual a diferença entre tabela fato e tabela dimensão?
   :::{dropdown} Resposta
   Fato guarda eventos mensuráveis (métricas numéricas + chaves), é grande; dimensão guarda o contexto descritivo (atributos textuais), é pequena e larga.
   :::
2. O que é o "grão" e por que declará-lo primeiro?
   :::{dropdown} Resposta
   O grão é o que uma linha da fato representa (ex.: um item de pedido). Declará-lo primeiro garante que métricas e dimensões sejam consistentes; misturar grãos gera números errados.
   :::
3. Star vs snowflake — qual Kimball prefere e por quê?
   :::{dropdown} Resposta
   Star (dimensões desnormalizadas), pela simplicidade e menos JOINs; o snowflake normaliza dimensões, economiza espaço mas adiciona complexidade raramente compensadora.
   :::
4. Cite os 4 passos de Kimball para modelar.
   :::{dropdown} Resposta
   1) Escolher o processo de negócio; 2) declarar o grão; 3) identificar as dimensões; 4) identificar os fatos (métricas).
   :::
5. Por que a dim_data é quase sempre necessária?
   :::{dropdown} Resposta
   Porque a maioria das análises é temporal (por dia/mês/trimestre/ano); uma dimensão de data rica (com ano, mês, feriado, dia da semana) habilita esses cortes sem recalcular.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Modele um star schema para um e-commerce."
  :::{dropdown} Resposta modelo
  Processo: vendas. Grão: um item de pedido. Fato `fato_vendas` (chaves para cliente, produto, data, loja; métricas quantidade e valor). Dimensões: `dim_cliente`, `dim_produto`, `dim_data`, `dim_loja`. Consultas agregam o fato juntando as dimensões necessárias.
  :::
- **P:** "Por que desnormalizar as dimensões, se isso repete dados?"
  :::{dropdown} Resposta modelo
  Porque em OLAP a leitura/análise domina; menos JOINs = consultas mais simples e rápidas, e modelos que o negócio entende. O custo de espaço da repetição é barato frente a esses ganhos.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kimball & Ross — The Data Warehouse Toolkit**, caps. 1–2 (fatos, dimensões, grão, 4 passos).
- **Reis & Housley — Fundamentals of Data Engineering**, cap. 8 (modelagem para consumo).

## 📚 Referências
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit*, 3ª ed. (2013) — cap. 1–2. <!-- @kimball2013 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 8. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 3 (modelos: estrela/floco). <!-- @kleppmann2017 -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
