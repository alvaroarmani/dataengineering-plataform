# BigQuery na prática: serverless, carga, partição/cluster e custo

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Até aqui os conceitos de DW (camadas, colunar, particionamento) você exercitou localmente no
DuckDB. Agora vamos ao **BigQuery** — o Data Warehouse serverless do Google Cloud, um dos
mais usados no mercado. A boa notícia: dá para praticar **de graça**, no *sandbox* (sem
cartão). Nesta unidade você cria um projeto, carrega o Olist, cria tabelas **particionadas e
clusterizadas de verdade** e mede o **custo por bytes varridos** — a habilidade que separa
quem "sabe SQL" de quem opera um DW cloud com consciência de custo.

## 💡 Conceito (o porquê)

### O modelo do BigQuery: serverless e separação storage/compute
Você **não gerencia servidor**. O BigQuery separa **armazenamento** (colunar, comprimido) de
**computação** (as *slots* que executam a query). Você não provisiona cluster; envia SQL e o
serviço aloca recursos. Consequência para o bolso: **paga-se pelo armazenamento** (por GB/mês)
**e pela consulta** — no modelo on-demand, por **bytes varridos** pela query.

### Sandbox free-tier (sem cartão)
O **BigQuery sandbox** deixa você criar um projeto e consultar **sem cadastrar cartão**, com
cotas gratuitas mensais (armazenamento e ~1 TB de consulta/mês). Tabelas no sandbox têm
expiração automática (60 dias) — perfeito para aprender. Passo a passo no lab desta unidade.

### Carregar dados
Formas comuns de trazer dados para uma tabela BigQuery:
- **Console web / `bq load`** a partir de CSV/JSON/Parquet (ex.: os CSVs do Olist).
- Carga de um bucket do **Cloud Storage** (padrão em produção).
- **`LOAD DATA` / consultas `CREATE TABLE AS`** para transformar durante a carga.

### Particionamento e clustering — de verdade
No BigQuery isso é declarativo e **real** (não simulado):

```sql
CREATE TABLE olist.fato_item_pedido
PARTITION BY DATE_TRUNC(data_pedido, MONTH)   -- partição por mês
CLUSTER BY categoria, estado                  -- ordena dentro da partição
AS SELECT ... ;
```

Ao filtrar pela **coluna de partição**, o BigQuery lê só as partições necessárias
(*partition pruning*); o **cluster** poda blocos por mín/máx nas colunas clusterizadas.
Menos bytes varridos ⇒ mais rápido **e** mais barato.

### Custo: pague pelo que varre
No modelo on-demand, o preço é por **bytes lidos pela query** (não pelo tamanho do resultado).
Duas ferramentas essenciais:
- **Estimativa (dry run):** o editor mostra "This query will process X GB" **antes** de rodar;
  no CLI, `bq query --dry_run`. Olhe sempre antes de executar.
- **Boas práticas de custo:** nunca `SELECT *`; selecione só as colunas; filtre pela coluna de
  partição; use `LIMIT` não reduz custo (varre igual) — o que reduz é **ler menos colunas e
  menos partições**.

## 🔎 Exemplo
Uma `fato_item_pedido` particionada por mês e clusterizada por `categoria`. A pergunta
"receita de eletrônicos em jan/2025":
```sql
SELECT SUM(price) AS receita
FROM olist.fato_item_pedido
WHERE data_pedido >= '2025-01-01' AND data_pedido < '2025-02-01'  -- poda partições
  AND categoria = 'eletronicos';                                   -- poda blocos (cluster)
```
O dry run mostra que a query varre uma fração ínfima da tabela — barata. Trocar por
`SELECT *` sem o filtro de data varreria a tabela inteira (caro).

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley descrevem os DWs cloud serverless (BigQuery/Snowflake) como a evolução que
separa armazenamento de computação e cobra por uso — deslocando o trabalho do engenheiro de
"administrar o cluster" para "modelar bem e controlar custo de consulta". — *Fundamentals of
Data Engineering*, cap. 6 e 8.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A própria documentação do BigQuery recomenda particionar por data e clusterizar as colunas
mais filtradas em tabelas grandes, e usar a **estimativa de bytes** antes de rodar — porque no
on-demand o custo é diretamente proporcional aos bytes varridos. — BigQuery, docs oficiais.
:::

## ⚠️ Erros comuns
- **`SELECT *`** numa tabela grande — varre todas as colunas, custo máximo.
- Rodar sem olhar a **estimativa (dry run)** — surpresa na fatura.
- Achar que **`LIMIT` reduz custo** — não reduz; a varredura acontece antes do limite.
- Não filtrar pela **coluna de partição** (ou aplicar função nela) — anula o pruning.
- Deixar tabelas temporárias/intermediárias crescendo sem expiração — custo de armazenamento.

## 💼 O que o mercado espera
Experiência com um **DW cloud real** e **consciência de custo** é das habilidades mais
valorizadas em vagas de Data Engineer. Saber criar tabela particionada/clusterizada e explicar
"por que essa query é barata" (via dry run) é assunto de entrevista e de code review no dia a dia.

:::{admonition} ✨ Em resumo
:class: resumo
- BigQuery é **serverless**: separa storage/compute; você paga **armazenamento + bytes varridos**.
- Pratique de graça no **sandbox** (sem cartão), com cotas mensais.
- Particione por data e **clusterize** as colunas mais filtradas — pruning real reduz custo.
- Sempre olhe a **estimativa (dry run)**; evite `SELECT *`; `LIMIT` não reduz custo.
:::

## 🧠 Quiz de recall
1. O que significa o BigQuery ser "serverless" e como isso afeta o custo?
   :::{dropdown} Resposta
   Você não gerencia servidor; ele separa armazenamento de computação e aloca recursos por query. Você paga pelo armazenamento (GB/mês) e pela consulta (bytes varridos no on-demand).
   :::
2. Como praticar BigQuery de graça sem cartão?
   :::{dropdown} Resposta
   Pelo BigQuery sandbox: cria projeto e consulta com cotas gratuitas mensais; tabelas expiram em 60 dias.
   :::
3. Como você reduz o custo de uma query no on-demand?
   :::{dropdown} Resposta
   Lendo menos bytes: selecione só as colunas necessárias (nada de SELECT *), filtre pela coluna de partição e use clustering nas colunas muito filtradas. LIMIT não ajuda.
   :::
4. Para que serve o dry run?
   :::{dropdown} Resposta
   Estimar quantos bytes a query vai varrer (e portanto o custo) ANTES de executá-la — no editor ou `bq query --dry_run`.
   :::
5. Como se declara partição e cluster no BigQuery?
   :::{dropdown} Resposta
   Na criação da tabela: `PARTITION BY DATE_TRUNC(coluna_data, MONTH)` e `CLUSTER BY col1, col2` (ex.: em `CREATE TABLE ... AS SELECT`).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Sua query no BigQuery está cara. Como investiga e corrige?"
  :::{dropdown} Resposta modelo
  Olho o dry run (bytes varridos), troco `SELECT *` pelas colunas necessárias, garanto o filtro pela coluna de partição (sem função em cima dela), e confirmo que a tabela está particionada por data e clusterizada nas colunas mais filtradas. Comparo o dry run antes/depois.
  :::
- **P:** "Por que `LIMIT 10` não deixou a query mais barata?"
  :::{dropdown} Resposta modelo
  Porque o custo é por bytes varridos no armazenamento colunar, e a varredura/filtragem acontece antes do LIMIT. Reduzir custo exige ler menos colunas e menos partições, não limitar o resultado.
  :::

## 🚀 Para ir além (leitura dirigida)
- **BigQuery docs** — *Introduction to partitioned tables* e *Clustered tables* (partição, cluster, custo).
- **Reis & Housley — Fundamentals of Data Engineering**, cap. 6 e 8 (storage/serving; DW cloud).

## 📚 Referências
- BigQuery — Documentação oficial (partição, clustering, controle de custos). <!-- @docs-bigquery -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 6 e 8. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 3 (colunar, custo de leitura). <!-- @kleppmann2017 -->

*Acessado em: 2026-08-24.*

---
**Revisado em:** 2026-08-24
