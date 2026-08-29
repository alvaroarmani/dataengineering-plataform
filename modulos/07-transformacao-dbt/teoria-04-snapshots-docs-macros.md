# Snapshots (SCD2), docs/lineage e macros no dbt

<!-- tipo: ferramenta -->

## 🎯 O problema (motivação)

Faltam três peças para o seu dbt virar o de um time de verdade: **preservar o histórico** de
dimensões que mudam (o SCD2 do M5, agora automático), **documentar** o projeto com um mapa de
**lineage** navegável, e **não repetir código** com **macros**. Esta unidade fecha o M7 com
essas três — as marcas de um projeto de dados maduro.

## 💡 Conceito (o porquê)

### Snapshots = SCD Tipo 2 automático
Fontes mudam **no lugar** (o cliente muda de cidade e o sistema sobrescreve). Um **snapshot**
do dbt captura o estado a cada execução e **versiona as mudanças** — implementando o SCD2 (M5)
sem você escrever o merge. Ele adiciona colunas de vigência: `dbt_valid_from`, `dbt_valid_to`
(null = versão atual) e `dbt_scd_id`.

```sql
{% snapshot snap_clientes %}
{{ config(
    target_schema='snapshots',
    unique_key='cliente_id',
    strategy='check',
    check_cols=['cidade']
) }}
select * from {{ source('olist', 'raw_clientes') }}
{% endsnapshot %}
```
- **`strategy='timestamp'`** — usa uma coluna `updated_at` para detectar mudança (preferida).
- **`strategy='check'`** — compara as colunas de `check_cols` (quando não há timestamp confiável).

Você roda com `dbt snapshot`. Na primeira vez, grava a versão atual; quando a cidade muda,
**fecha** a linha antiga (`dbt_valid_to`) e **insere** a nova — exatamente o SCD2.

### Docs e lineage
`dbt docs generate` produz um site; `dbt docs serve` o abre. Ele reúne as **descrições**
(dos `.yml`), os testes e — o mais valioso — o **grafo de lineage** (o DAG de `ref()`/`source()`),
que mostra visualmente de onde cada tabela vem e o que quebra se você mudar um model
(*impact analysis*).

### Macros e Jinja (não se repita)
O dbt compila **Jinja** antes do SQL. Um **macro** é um trecho SQL reutilizável:
```sql
{% macro centavos_para_reais(coluna) %}
    ({{ coluna }} / 100.0)
{% endmacro %}
```
usado em qualquer model: `select {{ centavos_para_reais('preco_centavos') }} as preco ...`.
Na prática, `ref()`, `source()` e `config()` **são macros**. O pacote **`dbt_utils`** traz
macros muito usados, como `generate_surrogate_key(['a','b'])` (hash → surrogate key) e `star`.

### Sources freshness
`dbt source freshness` avisa (ou falha) se a fonte está **desatualizada** além de um limite —
o primeiro sinal de observabilidade (M12): "os dados pararam de chegar?".

## 🔎 Exemplo
`snap_clientes` com `strategy='check'` em `cidade`: hoje grava `(ana, São Paulo)`. Semana que
vem a fonte diz `(ana, Campinas)` — o `dbt snapshot` fecha a linha de São Paulo
(`dbt_valid_to = agora`) e abre `(ana, Campinas)` como corrente. O fato pode então apontar
para a versão vigente na data da venda (M5). Tudo isso versionado e documentado no lineage.

:::{admonition} 📖 Da literatura
:class: seealso
Kimball define o SCD Tipo 2 como nova linha por versão, com datas de vigência e indicador de
corrente. Os **snapshots** do dbt automatizam exatamente esse padrão sobre fontes mutáveis —
trazendo a técnica clássica de DW para um fluxo declarativo e versionado. — *The Data Warehouse
Toolkit*, cap. 5 (SCDs).
:::

:::{admonition} 🏭 Do mundo real
:class: important
Times usam `dbt docs` + lineage para *impact analysis* (o que quebra se eu mudar este model?) e
`source freshness` como alerta de pipeline parado. Macros e `dbt_utils` mantêm centenas de
models DRY e consistentes. — dbt, documentação oficial.
:::

## ⚠️ Erros comuns
- Tentar fazer SCD2 "na mão" quando um **snapshot** resolve — reinventa a roda com bugs.
- `strategy='check'` com colunas demais (ou de menos) — versiona ruído ou perde mudanças reais.
- Models sem **descrição** nos `.yml` — o `dbt docs` fica vazio e o lineage, mudo.
- Abusar de macros/Jinja e tornar o SQL ilegível — use com parcimônia, para DRY real.
- Ignorar `source freshness` — o pipeline "passa" com dados velhos.

## 💼 O que o mercado espera
Saber quando usar snapshots (SCD2), gerar docs/lineage e escrever macros simples é o que separa
"escrevi uns SELECTs" de "mantenho um projeto dbt de produção". Lineage para impact analysis é
citado direto em entrevistas de Analytics Engineer.

:::{admonition} ✨ Em resumo
:class: resumo
- **Snapshots** = SCD2 automático: `dbt snapshot` versiona mudanças (dbt_valid_from/to), por
  `timestamp` ou `check`.
- **`dbt docs`** gera descrições + o **lineage** (DAG) navegável — base do *impact analysis*.
- **Macros/Jinja** deixam o SQL DRY; `ref`/`source` são macros; `dbt_utils` traz prontos (surrogate key).
- **`source freshness`** avisa quando os dados estão velhos (embrião de observabilidade).
:::

## 🧠 Quiz de recall
1. O que é um snapshot do dbt e qual padrão do M5 ele implementa?
   :::{dropdown} Resposta
   Um mecanismo que versiona mudanças de uma fonte mutável, implementando o SCD Tipo 2 (nova linha por versão, com dbt_valid_from/dbt_valid_to) automaticamente.
   :::
2. Diferença entre as strategies `timestamp` e `check`?
   :::{dropdown} Resposta
   timestamp usa uma coluna updated_at para detectar mudança; check compara as colunas de check_cols (quando não há timestamp confiável).
   :::
3. O que o `dbt docs` mais valioso oferece?
   :::{dropdown} Resposta
   O grafo de lineage (o DAG de ref/source), que mostra de onde vem cada tabela e o que quebra ao mudar um model (impact analysis), além das descrições e testes.
   :::
4. O que é um macro no dbt?
   :::{dropdown} Resposta
   Um trecho de SQL reutilizável escrito em Jinja ({% macro %}), chamado com {{ macro(...) }}. ref(), source() e config() são macros; dbt_utils traz vários prontos.
   :::
5. Para que serve `dbt source freshness`?
   :::{dropdown} Resposta
   Avisar ou falhar se a fonte está desatualizada além de um limite — sinal de pipeline parado (observabilidade).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você preserva o histórico de uma dimensão que muda, no dbt?"
  :::{dropdown} Resposta modelo
  Com um snapshot: configuro unique_key e a strategy (timestamp se houver updated_at, senão check nas colunas relevantes). O dbt snapshot fecha a versão antiga e abre a nova a cada mudança, gerando um SCD2 com dbt_valid_from/to — sem escrever o merge manualmente.
  :::
- **P:** "Para que serve o lineage do dbt no dia a dia?"
  :::{dropdown} Resposta modelo
  Para impact analysis e debugging: vejo de onde cada tabela vem e o que depende dela, então sei o que testar/quebrar ao alterar um model, e rastreio a origem de um número errado subindo o grafo.
  :::

## 🚀 Para ir além (leitura dirigida)
- **dbt docs** — *Snapshots*, *Documentation*, *Jinja & macros*, *dbt_utils*, *Source freshness*.
- **Kimball & Ross — The Data Warehouse Toolkit**, cap. 5 (SCD2 — a base dos snapshots).

## 📚 Referências
- dbt — Documentação oficial (snapshots, docs/lineage, macros/Jinja, source freshness). <!-- @docs-dbt -->
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit*, 3ª ed. (2013) — cap. 5 (SCD2). <!-- @kimball2013 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 8 (transformação, lineage). <!-- @reis2022 -->

*Acessado em: 2026-08-24.*

---
**Revisado em:** 2026-08-24
