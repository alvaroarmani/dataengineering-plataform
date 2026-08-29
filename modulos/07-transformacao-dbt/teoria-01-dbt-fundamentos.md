# dbt: transformação como código (ELT, sources e staging)

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Você já sabe modelar (M5) e já tem um DW (M6). Falta a peça que as empresas usam para
**transformar** os dados crus em tabelas prontas para análise, de forma **versionada, testada
e documentada**: o **dbt** (data build tool). Em vez de scripts SQL soltos e frágeis, o dbt
transforma o "T" do ELT numa base de código de engenharia — com dependências, testes e
lineage. É a ferramenta que quase toda vaga de Analytics/Data Engineer pede hoje.

## 💡 Conceito (o porquê)

### O "T" do ELT — transformar dentro do warehouse
No **ELT** (Extract-Load-**Transform**), você primeiro **carrega** os dados crus no DW e só
então **transforma**, usando o poder de processamento do próprio warehouse (Postgres, BigQuery).
O dbt é a ferramenta desse T: você escreve **`SELECT`s**, e o dbt cuida de criar as tabelas/
views, na ordem certa, com testes e documentação.

### Um "model" é um SELECT
No dbt, cada **model** é um arquivo `.sql` com **um `SELECT`**. O dbt materializa o resultado
como uma **view** (padrão) ou **table** no DW. Você nunca escreve `CREATE TABLE ...` — descreve
o *resultado* que quer, e o dbt gera o DDL.

### sources e ref() — o grafo de dependências
- **`source()`** aponta para as tabelas **cruas** (o que foi carregado no schema `raw`),
  declaradas em um `sources.yml`.
- **`ref('outro_model')`** referencia **outro model** dbt. Isso constrói um **DAG** de
  dependências: o dbt descobre a ordem de execução e desenha o **lineage** automaticamente.

```{mermaid}
flowchart LR
    R[(raw.pedidos<br/>source)] --> S[stg_pedidos<br/>staging] --> M[mart_receita<br/>mart] --> BI[BI]
```

### Camada de staging
Convenção dbt (que ecoa as camadas do M6): **staging** models (`stg_*`) fazem a limpeza leve
1:1 com a fonte — renomear colunas, converter tipos, padronizar — sem regras de negócio. Depois
os **marts** (dimensional) combinam staging models em fatos/dimensões.

### Materializations
Como o resultado é persistido, definido por model ou pasta:
- **view** (padrão): leve, sempre fresca, recomputa ao consultar.
- **table**: materializa fisicamente (mais rápido de ler, recomputado a cada run).
- **incremental**: só processa o que mudou (grandes volumes).
- **ephemeral**: vira CTE, não cria objeto no DW.

### Comandos essenciais
- `dbt seed` — carrega CSVs de `seeds/` como tabelas (dados de exemplo versionados).
- `dbt run` — materializa os models.
- `dbt test` — roda os testes de dados (ver próxima unidade).
- **`dbt build`** — faz tudo na ordem do DAG: seed → run → test → snapshot. É o comando do dia a dia.

## 🔎 Exemplo
Uma tabela crua `raw.pedidos(id, cliente, uf, valor_str)`. O staging model `stg_pedidos.sql`:
```sql
select
    cast(id as integer)        as pedido_id,
    cliente,
    upper(uf)                  as estado,
    cast(valor_str as numeric) as valor
from {{ source('olist', 'pedidos') }}
```
`dbt run` cria a view `stg_pedidos` no DW. Um mart depois faz `... from {{ ref('stg_pedidos') }}`.
O dbt sabe que o mart depende do staging, que depende do source — e roda tudo na ordem certa.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley situam o dbt no paradigma **ELT**: com os DWs cloud baratos e elásticos, virou
prático carregar cru e transformar dentro do warehouse, versionando as transformações como
código — trazendo testes, revisão e CI para o mundo de dados ("analytics engineering"). —
*Fundamentals of Data Engineering*, cap. 8.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A documentação do dbt recomenda a arquitetura em camadas **staging → intermediate → marts**,
com `ref()`/`source()` construindo o lineage — exatamente o que times de dados usam para manter
centenas de models organizados e testados. — dbt, documentação oficial.
:::

## ⚠️ Erros comuns
- Escrever `CREATE TABLE` no model — no dbt você descreve **o `SELECT`**; a materialização é dele.
- Referenciar a tabela crua direto (`from raw.pedidos`) em vez de `{{ source(...) }}` — perde lineage e testes de source.
- Pular a camada **staging** e colocar regra de negócio já no primeiro model — vira bagunça.
- Usar `table` onde `view` bastava (ou vice-versa) sem pensar em custo/frescor.
- Esquecer `dbt seed` — os models falham porque a fonte não existe no DW.

## 💼 O que o mercado espera
dbt é **requisito recorrente** em vagas de Analytics/Data Engineer. Saber estruturar um projeto
(sources, staging, marts), usar `ref()`/`source()` e rodar `dbt build` é o mínimo esperado —
e é o que você faz no dia a dia de um time de dados moderno.

:::{admonition} ✨ Em resumo
:class: resumo
- dbt é o **"T" do ELT**: você escreve `SELECT`s (models); ele materializa (view/table),
  na ordem do **DAG**, com testes e docs.
- **`source()`** = tabela crua; **`ref()`** = outro model → constrói lineage automático.
- Camadas: **staging** (`stg_*`, limpeza 1:1) → **marts** (dimensional).
- Comando do dia a dia: **`dbt build`** (seed → run → test → snapshot).
:::

## 🧠 Quiz de recall
1. O que é o dbt e qual parte do ELT ele cobre?
   :::{dropdown} Resposta
   É a ferramenta de transformação (o "T" do ELT): você escreve SELECTs e ele materializa tabelas/views no warehouse, com dependências, testes e docs.
   :::
2. O que é um "model" no dbt?
   :::{dropdown} Resposta
   Um arquivo .sql com um SELECT; o dbt gera o DDL e materializa o resultado (view por padrão) no DW. Você não escreve CREATE TABLE.
   :::
3. Diferença entre `source()` e `ref()`?
   :::{dropdown} Resposta
   `source()` referencia tabelas cruas declaradas em sources.yml; `ref()` referencia outro model dbt. Juntos constroem o DAG de dependências e o lineage.
   :::
4. O que faz `dbt build`?
   :::{dropdown} Resposta
   Executa na ordem do DAG: seed (carrega CSVs), run (materializa models), test (roda testes) e snapshot — tudo de uma vez.
   :::
5. Para que serve a camada de staging?
   :::{dropdown} Resposta
   Limpeza leve 1:1 com a fonte (renomear, converter tipos, padronizar), sem regra de negócio — base para os marts dimensionais.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que ELT (dbt) em vez de ETL tradicional?"
  :::{dropdown} Resposta modelo
  Porque os DWs cloud são baratos e elásticos: carregar cru e transformar dentro do warehouse aproveita esse poder, e o dbt versiona as transformações como código, com testes, revisão e CI. Ganha-se manutenibilidade e confiança frente a scripts ETL soltos.
  :::
- **P:** "Como o dbt sabe a ordem de execução dos models?"
  :::{dropdown} Resposta modelo
  Pelo grafo de dependências: cada `ref()`/`source()` cria uma aresta; o dbt monta o DAG e executa os models em ordem topológica, o que também gera o lineage.
  :::

## 🚀 Para ir além (leitura dirigida)
- **dbt docs** — *About dbt projects*, *Sources*, *Materializations* (fundamentos do projeto).
- **Reis & Housley — Fundamentals of Data Engineering**, cap. 8 (ELT, analytics engineering).

## 📚 Referências
- dbt — Documentação oficial (projetos, sources, models, materializations). <!-- @docs-dbt -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 8 (ELT, transformação). <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — transformação e padrões de pipeline. <!-- @densmore2021 -->

*Acessado em: 2026-08-24.*

---
**Revisado em:** 2026-08-24
