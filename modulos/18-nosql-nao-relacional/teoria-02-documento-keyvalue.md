# Documento (MongoDB) e key-value (Redis)

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Das quatro famílias (unidade 1), duas resolvem a maior parte dos casos do dia a dia e você vai
encontrá-las em quase toda arquitetura: **documento** (MongoDB) para dados com estrutura rica e
variável, e **key-value** (Redis) para velocidade extrema em cache e sessões. Entender **como
modelar** em cada uma — e quando NÃO usá-las — é o que separa "ouvi falar de MongoDB" de "sei
projetar com bancos de documento e de cache".

## 💡 Conceito (o porquê)

### Banco de documento (MongoDB)
Um banco de documento guarda **documentos** — objetos JSON/BSON com campos, aninhamento e arrays.
Uma **coleção** é um conjunto de documentos (o análogo de uma tabela), mas **sem esquema fixo**: dois
documentos da mesma coleção podem ter campos diferentes.
```json
{ "_id": 1, "nome": "Camiseta", "preco": 49.9,
  "atributos": { "cor": "azul", "tamanhos": ["P","M","G"] },
  "avaliacoes": [ { "nota": 5 }, { "nota": 4 } ] }
```
**Vantagem:** o dado que a aplicação usa junto **fica junto** (aninhado), então ler um produto é uma
única busca — sem JOINs. **Modelagem por agregado:** você desenha o documento em torno do que a
aplicação lê de uma vez.

### Embutir (embed) vs referenciar (reference)
A decisão central de modelagem em documento:
- **Embutir:** aninhar os dados relacionados dentro do documento (as avaliações dentro do produto).
  Ótimo quando são lidos juntos e não crescem sem limite. Leitura em uma tocada.
- **Referenciar:** guardar só o **id** de outro documento (como uma FK) e buscar à parte. Melhor
  quando o relacionado é grande, muda muito, ou é compartilhado por muitos.

Regra prática: **embute o que se lê junto e é limitado; referencia o que é grande, volátil ou compartilhado.**

### Consultas e agregação
Além de buscas por campo (inclusive dentro de subdocumentos e arrays), bancos de documento têm um
**pipeline de agregação**: estágios encadeados (`match` → `group` → `sort` …) que fazem o análogo do
`WHERE`/`GROUP BY`/`ORDER BY` do SQL, mas sobre documentos. É como você calcula "vendas por
categoria" sem SQL.

### Índices continuam importando
Assim como no relacional (M04), consultas sem índice varrem a coleção inteira. Bancos de documento
indexam campos (inclusive aninhados) — sem o índice certo, o NoSQL também fica lento. NoSQL não
dispensa pensar em índices.

### Key-value (Redis)
Um banco key-value é um **dicionário distribuído**: você guarda um **valor** sob uma **chave** e o
recupera por ela — sem consultas por conteúdo. É extremamente rápido (muitas vezes **em memória**),
com latência de microssegundos a poucos milissegundos. O Redis ainda oferece **TTL** (expiração
automática de chaves) e estruturas prontas (listas, sets, contadores).

Casos clássicos: **cache** (guardar o resultado caro de uma consulta/página por alguns minutos),
**sessões** de usuário, **contadores** e **rate limiting**, filas simples. O padrão *cache-aside*:
a aplicação procura no Redis; se não achar (*miss*), busca no banco principal, grava no Redis com um
**TTL** e devolve — as próximas leituras vêm do cache até expirar.

### Quando NÃO usar
- **Documento:** relacionamentos muitos-para-muitos complexos, transações across-múltiplos-agregados,
  ou análises ad-hoc com muitos JOINs — o relacional serve melhor.
- **Key-value:** qualquer consulta por conteúdo (só busca por chave) ou dado que precisa durar como
  fonte da verdade — cache é efêmero por natureza.

## 🔎 Exemplo
No e-commerce: o **catálogo** vive no MongoDB — cada produto é um documento com atributos e avaliações
**embutidas** (lidas juntas), enquanto o **vendedor** é **referenciado** por id (é grande e
compartilhado por muitos produtos). Para o painel "nota média por categoria", um **pipeline de
agregação** faz `match`→`group`. Já o **carrinho** e o cache das páginas de produto vivem no **Redis**,
com TTL de minutos: a primeira visita popula o cache (miss), as seguintes voltam em 1ms (hit) até
expirar. Um documento para estrutura rica, um key-value para velocidade — cada um no seu lugar.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann analisa o **modelo de documento** (localidade do agregado, embutir vs referenciar, a volta
das limitações de JOIN) e discute caches e armazenamento em memória entre os sistemas de dados. — 
*Designing Data-Intensive Applications* (cap. 2).
:::

:::{admonition} 🏭 Do mundo real
:class: important
Redis na frente do banco principal é um dos padrões mais comuns de escala: absorve o grosso das
leituras repetidas com latência mínima. E o erro mais comum em MongoDB é **modelar como no
relacional** (tudo normalizado, "juntando" na aplicação) em vez de aproveitar o agregado embutido —
resultado: muitas idas ao banco e performance pior que o Postgres que se queria substituir. — prática
de mercado; Kleppmann.
:::

## ⚠️ Erros comuns
- **Modelar documento normalizado** como no relacional, em vez de embutir o que se lê junto.
- **Embutir dados que crescem sem limite** (ex.: todos os logs num documento) — estoura o tamanho.
- **Achar que NoSQL dispensa índice** — consultas sem índice varrem a coleção.
- **Usar Redis como fonte da verdade** — é cache/efêmero; sem persistência garantida, some.
- **Cache sem TTL nem invalidação** — serve dado velho para sempre.

## 💼 O que o mercado espera
Modelar em documento (embed vs reference, agregação), usar Redis para cache/sessão com TTL e o padrão
cache-aside, e saber quando cada um **não** serve. Aparece em system design ("como você adicionaria
cache?") e em vagas que citam MongoDB/Redis.

:::{admonition} ✨ Em resumo
:class: resumo
- **Documento (MongoDB)**: JSON aninhado, esquema flexível; modele **pelo agregado** — embute o que se lê junto, referencia o grande/compartilhado.
- **Agregação** (pipeline de estágios) faz o papel de GROUP BY; **índices** continuam essenciais.
- **Key-value (Redis)**: dicionário em memória, latência mínima; cache/sessão/contador com **TTL** (padrão cache-aside).
- Redis é **efêmero** (não é fonte da verdade); documento não substitui relacional em JOINs/transações complexas.
:::

## 🧠 Quiz de recall
1. O que é um documento e uma coleção no MongoDB?
   :::{dropdown} Resposta
   Um documento é um objeto JSON/BSON com campos aninhados; uma coleção é um conjunto de documentos (análogo à tabela), sem esquema fixo.
   :::
2. Quando embutir e quando referenciar?
   :::{dropdown} Resposta
   Embutir o que é lido junto e limitado (aninhar); referenciar (guardar só o id) o que é grande, muda muito ou é compartilhado por muitos.
   :::
3. Para que serve o pipeline de agregação?
   :::{dropdown} Resposta
   Encadear estágios (match, group, sort…) para consultas analíticas sobre documentos — o análogo de WHERE/GROUP BY/ORDER BY do SQL.
   :::
4. Qual o caso de uso e a característica-chave do Redis?
   :::{dropdown} Resposta
   Cache, sessões, contadores; é um key-value em memória, com latência mínima e TTL (expiração automática). Busca só por chave.
   :::
5. O que é o padrão cache-aside?
   :::{dropdown} Resposta
   A aplicação procura no cache; no miss, busca no banco principal, grava no cache com TTL e devolve; as próximas leituras vêm do cache até expirar.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você modelaria um catálogo de produtos com avaliações no MongoDB?"
  :::{dropdown} Resposta modelo
  Cada produto é um documento; embuto os atributos e as avaliações que leio junto com o produto (localidade do agregado), mas referencio por id o que é grande ou compartilhado, como o vendedor. Crio índices nos campos consultados (nome, categoria). Para "nota média por categoria", uso o pipeline de agregação (match→group). Evito embutir coisas que crescem sem limite.
  :::
- **P:** "Onde você adicionaria Redis numa arquitetura e por quê?"
  :::{dropdown} Resposta modelo
  Na frente do banco principal, como cache-aside: guardo resultados caros de consulta/página e sessões com TTL. Absorve as leituras repetidas com latência mínima e alivia o banco. Trato o Redis como efêmero (não fonte da verdade) e defino invalidação/TTL para não servir dado velho.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (cap. 2, modelo de documento).
- **Documentação do MongoDB** — modelagem de dados e aggregation pipeline.
- **Documentação do Redis** — estruturas, TTL e padrões de cache.

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — modelo de documento. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — armazenamento e cache. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — fontes NoSQL em pipelines. <!-- @densmore2021 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
