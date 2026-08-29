# Testes de dados no dbt (a rede de segurança do pipeline)

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Um pipeline que roda "sem erro" ainda pode entregar **dados errados**: uma chave duplicada,
um nulo onde não podia, uma venda apontando para um produto que não existe. No dbt, você
declara **testes de dados** que rodam a cada `build` — e falham antes que o número errado
chegue no dashboard. É uma das razões de o dbt ter conquistado o mercado: transforma
qualidade de dados em **código versionado e automático**.

## 💡 Conceito (o porquê)

### Testes genéricos (out-of-the-box)
Declarados no `schema.yml`, por coluna. Os quatro essenciais:

- **`not_null`** — a coluna não pode ter nulos.
- **`unique`** — os valores são únicos (ex.: a chave da dimensão).
- **`accepted_values`** — o valor está numa lista permitida (ex.: `status in ('pago','cancelado')`).
- **`relationships`** — **integridade referencial**: todo valor existe na outra tabela (ex.:
  toda `produto_id` do fato existe em `dim_produto`).

```yaml
models:
  - name: fct_item_pedido
    columns:
      - name: pedido_id
        tests: [not_null, unique]
      - name: produto_id
        tests:
          - relationships:
              to: ref('dim_produto')
              field: produto_id
      - name: status
        tests:
          - accepted_values:
              values: ['pago', 'cancelado', 'enviado']
```

### Como um teste funciona por baixo
Um teste dbt é **uma query que busca as linhas que violam a regra**. Se ela retorna **zero
linhas**, o teste **passa**; se retorna alguma, **falha** (e o dbt mostra quantas). É por isso
que testar é barato e objetivo — é SQL.

### Testes singulares (custom)
Regras específicas do negócio viram um arquivo `.sql` em `tests/` com um `SELECT` que retorna
o que **não deveria existir**:
```sql
-- tests/receita_nao_negativa.sql
select * from {{ ref('fct_receita_categoria') }} where receita < 0
```
Se algum dia uma receita ficar negativa, o `dbt test` falha.

### Pacotes: dbt_utils
O pacote **`dbt_utils`** adiciona testes prontos muito usados (ex.:
`expression_is_true`, `accepted_range`, `unique_combination_of_columns`) e macros — instalado
via `packages.yml` + `dbt deps`.

### Severity e onde rodam
Cada teste tem **severity** (`error` barra o build; `warn` só avisa). `dbt test` roda todos;
`dbt build` roda os testes **junto** com os models, no DAG — se um staging falha, o mart
dependente nem roda.

## 🔎 Exemplo
No star do Olist: `unique`+`not_null` na chave de `dim_produto`; `relationships` de
`fct_item_pedido.produto_id → dim_produto.produto_id`. Se uma carga trouxer um item com
`produto_id` inexistente na dimensão, o teste `relationships` falha no build — o bug é pego na
hora, não três dashboards depois.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley colocam **qualidade e testes** entre as *undercurrents* da engenharia de dados:
dados sem testes são dados em que ninguém confia. Ferramentas como o dbt trazem testes
declarativos para o pipeline, aproximando dados das práticas de engenharia de software. —
*Fundamentals of Data Engineering* (qualidade de dados; cap. 8).
:::

:::{admonition} 🏭 Do mundo real
:class: important
A documentação do dbt trata testes como parte do fluxo padrão (`dbt build` roda models + testes
no DAG), e times maduros bloqueiam o merge/deploy se algum teste `error` falha — o embrião dos
**data contracts** e da observabilidade (M12). — dbt, docs oficiais.
:::

## ⚠️ Erros comuns
- Não testar a **chave** da dimensão (`unique`+`not_null`) — duplicatas inflam o fato no join.
- Esquecer `relationships` — fatos "órfãos" (FK inexistente) passam silenciosos.
- Testes só como `warn` para tudo — o build "passa" com dados quebrados.
- Regra de negócio importante sem **teste singular** — some numa refatoração.
- Rodar `dbt run` sem `dbt test` — materializa sem validar (use **`dbt build`**).

## 💼 O que o mercado espera
Saber declarar e justificar testes (especialmente `relationships` e `unique`) é diferencial
forte de Analytics Engineer. "Como você garante a qualidade dos seus models?" é pergunta de
entrevista — e a resposta certa passa por testes no dbt + CI.

:::{admonition} ✨ Em resumo
:class: resumo
- Testes genéricos no `schema.yml`: **not_null, unique, accepted_values, relationships** (FK).
- Um teste é **uma query que busca violações**: 0 linhas = passa.
- Regras de negócio viram **testes singulares** (`tests/*.sql`); `dbt_utils` traz mais prontos.
- `dbt build` roda models + testes no DAG; use `severity: error` para barrar dados quebrados.
:::

## 🧠 Quiz de recall
1. Cite os quatro testes genéricos do dbt e o que cada um faz.
   :::{dropdown} Resposta
   not_null (sem nulos), unique (valores únicos), accepted_values (valor numa lista permitida), relationships (integridade referencial — o valor existe na outra tabela).
   :::
2. Como um teste dbt decide passar ou falhar?
   :::{dropdown} Resposta
   O teste é uma query que retorna as linhas que violam a regra; 0 linhas = passa, qualquer linha = falha (o dbt mostra quantas).
   :::
3. O que é um teste singular (custom)?
   :::{dropdown} Resposta
   Um SELECT em tests/*.sql que retorna o que não deveria existir (ex.: receita < 0). Se retornar algo, o dbt test falha.
   :::
4. Qual teste pega um fato apontando para um produto inexistente?
   :::{dropdown} Resposta
   `relationships` (integridade referencial): valida que todo produto_id do fato existe em dim_produto.
   :::
5. Diferença entre severity `error` e `warn`?
   :::{dropdown} Resposta
   error barra o build (falha); warn só emite aviso e o build segue.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você garante a qualidade dos dados nos seus models dbt?"
  :::{dropdown} Resposta modelo
  Testo as chaves (unique+not_null nas dimensões), integridade referencial (relationships dos fatos para as dimensões), domínios (accepted_values) e regras de negócio críticas com testes singulares. Rodo tudo no `dbt build` dentro do CI, com severity error barrando o deploy se algo quebra.
  :::
- **P:** "Um teste `unique` está falhando na dimensão. O que isso indica?"
  :::{dropdown} Resposta modelo
  Que há chaves duplicadas — provavelmente o grão da dimensão está errado ou a fonte trouxe duplicatas. Isso é grave: no join com o fato, duplicaria linhas e inflaria as métricas. Investigo a origem e corrijo o grão/dedup antes de seguir.
  :::

## 🚀 Para ir além (leitura dirigida)
- **dbt docs** — *Add tests to your DAG*, *Generic tests*, *Singular tests*, *dbt_utils*.
- **Reis & Housley — Fundamentals of Data Engineering** — qualidade de dados (undercurrents).

## 📚 Referências
- dbt — Documentação oficial (tests genéricos, singulares, dbt_utils, build). <!-- @docs-dbt -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — qualidade de dados; cap. 8. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — validação e confiabilidade de pipelines. <!-- @densmore2021 -->

*Acessado em: 2026-08-24.*

---
**Revisado em:** 2026-08-24
