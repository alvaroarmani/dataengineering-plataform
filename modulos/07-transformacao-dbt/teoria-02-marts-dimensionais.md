# Marts dimensionais com dbt (ref, camadas e o star schema)

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Na U1 você limpou os dados numa camada de **staging**. Mas o staging ainda não é o que o
negócio consome — falta montar o **star schema** (fatos e dimensões, do M5) em cima dele. É
o papel dos **marts**: os models de consumo. Nesta unidade você encadeia `staging → marts` com
`ref()`, deixando o dbt orquestrar o DAG — exatamente como um projeto de dados real cresce.

## 💡 Conceito (o porquê)

### As camadas de um projeto dbt
A convenção (que ecoa staging→core→marts do M6):

- **staging (`stg_*`)** — limpeza 1:1 com a fonte (feito na U1).
- **intermediate (`int_*`)** — passos intermediários reutilizáveis (joins, agregações parciais). Opcional.
- **marts (`fct_*` / `dim_*`)** — as tabelas de consumo: **fatos e dimensões** dimensionais.

Cada camada referencia a anterior com `ref()`, nunca a fonte crua diretamente.

### `ref()` encadeia os models (e constrói o DAG)
Um mart lê **outros models**, não a tabela crua:
```sql
-- fct_receita_categoria.sql
select p.categoria, sum(i.price) as receita
from {{ ref('stg_itens') }} i
join {{ ref('stg_produtos') }} p on i.produto_id = p.produto_id
group by p.categoria
```
Cada `ref()` cria uma aresta no DAG. O dbt descobre que `fct_receita_categoria` depende de
`stg_itens` e `stg_produtos`, roda-os primeiro, e desenha o **lineage** automaticamente.

```{mermaid}
flowchart LR
    RI[(raw_itens)] --> SI[stg_itens]
    RP[(raw_produtos)] --> SP[stg_produtos]
    SI --> F[fct_receita_categoria]
    SP --> F
    F --> BI[BI]
```

### Fatos e dimensões como models
O M5 fica direto: cada **dimensão** (`dim_produto`, `dim_cliente`) e cada **fato**
(`fct_item_pedido`) vira um model dbt na camada marts. A **surrogate key** (M5-U2) costuma ser
gerada no mart com um pacote (`dbt_utils.generate_surrogate_key`) ou `row_number()`.

### Materialização dos marts
Marts costumam ser **`table`** (materializados fisicamente), pois são lidos muitas vezes por
dashboards — vale o custo de recomputar no build para consultas rápidas depois. Staging pode
ficar como **`view`** (leve, sempre fresco). Você configura por pasta no `dbt_project.yml`:
```yaml
models:
  meu_projeto:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

## 🔎 Exemplo
Do staging `stg_itens` (item, produto_id, price) + `stg_produtos` (produto_id, categoria),
o mart `fct_receita_categoria` junta por `produto_id` e soma `price` por categoria. O dbt roda
`stg_itens` e `stg_produtos` antes do fato, porque o `ref()` disse a ordem. Amanhã, um mart de
`fct_receita_estado` reaproveita os mesmos staging models — sem recolar a limpeza.

:::{admonition} 📖 Da literatura
:class: seealso
Kimball define os marts como a camada de consumo em star schema — fatos e dimensões que o
negócio entende. O dbt materializa essa camada a partir de models encadeados, com testes e
lineage, tornando a construção do star **versionada e reprodutível**. — *The Data Warehouse
Toolkit*, cap. 1–2 (marts, dimensional).
:::

:::{admonition} 🏭 Do mundo real
:class: important
A documentação do dbt recomenda `staging → intermediate → marts` com um model por arquivo e
`ref()` entre camadas — a organização que mantém projetos com centenas de models navegáveis e
testáveis, e gera o lineage que os times usam para *impact analysis*. — dbt, docs oficiais.
:::

## ⚠️ Erros comuns
- Um mart lendo a **fonte crua** (`from raw_itens`) em vez de `{{ ref('stg_...') }}` — quebra camadas e lineage.
- Colocar **regra de negócio no staging** — staging é 1:1; regra vai no mart/intermediate.
- Materializar marts pesados como `view` — dashboards ficam lentos (recomputam sempre).
- Um model gigante fazendo tudo — prefira **um model por passo** (staging, intermediate, mart).
- Esquecer testes no mart (grão/unicidade da dimensão) — bugs silenciosos a jusante.

## 💼 O que o mercado espera
Montar marts em star schema com dbt (`ref()`, materialização certa, testes) é o trabalho
central de um Analytics Engineer. Saber justificar as camadas e o lineage diferencia — é o que
mantém o projeto de dados de uma empresa sustentável.

:::{admonition} ✨ Em resumo
:class: resumo
- Marts são a camada de **consumo** (fatos/dimensões do star), construída sobre o staging.
- Use **`ref('stg_...')`** (nunca a fonte crua) — cada `ref()` monta o DAG e o lineage.
- Camadas: `stg_*` (view) → `int_*` (opcional) → `fct_*`/`dim_*` (table).
- Um model por passo; teste o grão/unicidade nos marts.
:::

## 🧠 Quiz de recall
1. Quais são as camadas típicas de um projeto dbt?
   :::{dropdown} Resposta
   staging (stg_*, limpeza 1:1), intermediate (int_*, opcional) e marts (fct_*/dim_*, consumo dimensional). Cada uma referencia a anterior com ref().
   :::
2. Por que um mart usa `ref('stg_...')` e não a tabela crua?
   :::{dropdown} Resposta
   Para respeitar as camadas e construir o DAG/lineage: o dbt roda o staging antes do mart e sabe as dependências. Ler a crua direto quebra isso e reaproveitamento.
   :::
3. Como o dbt sabe rodar o staging antes do fato?
   :::{dropdown} Resposta
   Pelo `ref()`: cada referência vira aresta no DAG; o dbt executa em ordem topológica (dependências primeiro).
   :::
4. Qual materialização faz sentido para staging vs marts, e por quê?
   :::{dropdown} Resposta
   Staging como view (leve, sempre fresco); marts como table (lidos muitas vezes por dashboards, vale materializar para consultas rápidas).
   :::
5. Onde vai a regra de negócio: staging ou mart?
   :::{dropdown} Resposta
   No mart (ou intermediate). Staging é limpeza 1:1 sem regra de negócio.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você organizaria um projeto dbt para um e-commerce?"
  :::{dropdown} Resposta modelo
  Camada staging (stg_pedidos, stg_itens, stg_produtos, stg_clientes — limpeza 1:1 das fontes), talvez intermediate para joins reutilizáveis, e marts com o star: dim_produto, dim_cliente, dim_data e fct_item_pedido no grão do item. `ref()` entre camadas, staging como view e marts como table, com testes de grão e relacionamento.
  :::
- **P:** "Por que não fazer um único model que junta tudo?"
  :::{dropdown} Resposta modelo
  Porque perde reaproveitamento, testabilidade e legibilidade. Um model por passo deixa o DAG claro, permite testar cada camada e reusar o staging em vários marts — como funções pequenas em código.
  :::

## 🚀 Para ir além (leitura dirigida)
- **dbt docs** — *How we structure our dbt projects* (staging/intermediate/marts) e *ref*.
- **Kimball & Ross — The Data Warehouse Toolkit**, caps. 1–2 (marts, fatos e dimensões).

## 📚 Referências
- dbt — Documentação oficial (estrutura de projeto, ref, materializations). <!-- @docs-dbt -->
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit*, 3ª ed. (2013) — cap. 1–2 (marts dimensionais). <!-- @kimball2013 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 8 (camadas de consumo). <!-- @reis2022 -->

*Acessado em: 2026-08-24.*

---
**Revisado em:** 2026-08-24
