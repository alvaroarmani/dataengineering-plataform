# Testes de dados: dbt e Great Expectations

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

As dimensões de qualidade (U1) só valem se viram **testes automáticos** que rodam a cada carga.
Duas ferramentas dominam: o **dbt** (testes acoplados aos models, M7) e o **Great Expectations
(GE)** (uma suíte de validação independente, para dados que não passam pelo dbt). Saber qual
usar — e escrever os testes — é a parte prática da qualidade.

## 💡 Conceito (o porquê)

### Testes no dbt (recap do M7, aplicado)
No `schema.yml`, por coluna: **`not_null`**, **`unique`**, **`accepted_values`**,
**`relationships`** (FK). Regras de negócio viram **testes singulares** (`tests/*.sql` que
retornam as linhas inválidas — 0 = passa). Rodam no `dbt build`, dentro do DAG. Ideal quando o
dado **já está no warehouse** e é transformado por dbt.

### Great Expectations (GE)
GE é uma biblioteca de **validação de dados** independente do dbt. Você declara **expectations**
("expectativas") sobre um dataset:
- `expect_column_values_to_not_be_null`, `expect_column_values_to_be_unique`,
  `expect_column_values_to_be_in_set`, `expect_column_values_to_be_between`, etc.
Um conjunto vira uma **suíte**; rodar gera um **Data Docs** (relatório) e falha se as
expectativas não baterem. Útil **na ingestão** (validar um arquivo/carga **antes** de gravar) e
para dados fora do dbt.

### dbt vs GE — quando cada um
- **dbt tests:** dados já no DW, transformados por dbt; testes versionados junto dos models.
- **GE:** validar **na fronteira** (arquivo recém-chegado, uma API), dados que não passam pelo
  dbt, ou suítes ricas com relatório. Muitos times usam **os dois** (GE na ingestão, dbt no DW).

### O que todo teste faz por baixo
Independente da ferramenta, um teste é **uma consulta que busca as violações**: 0 violações =
passa. É a mesma ideia do M7 — o que muda é onde e como você declara.

## 🔎 Exemplo
Ingestão do Olist: uma suíte **GE** valida o CSV recém-baixado (colunas presentes,
`pedido_id` único, `valor` ≥ 0) **antes** de carregar — barra o arquivo ruim na porta. Depois,
no DW, os **dbt tests** garantem `relationships` do fato para as dimensões. Dois pontos de
checagem: fronteira (GE) e consumo (dbt).

:::{admonition} 📖 Da literatura
:class: seealso
A documentação do dbt trata testes como parte do fluxo (`dbt build`), e o Great Expectations
propõe declarar **expectations** versionadas com relatório (Data Docs) — ambos materializam o
princípio "um teste é uma checagem executável de qualidade". — dbt, docs oficiais.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Times combinam **GE na ingestão** (validar dados crus antes de gravar) e **dbt tests no DW**
(integridade dos models) — cobrindo a fronteira e o consumo. Falhas viram alerta e bloqueiam o
deploy no CI (M13). — dbt / Great Expectations, docs oficiais.
:::

## ⚠️ Erros comuns
- Só testar no DW (dbt) e deixar **dado ruim entrar** — falta validar na ingestão (GE).
- Testes só como **warn** — o build "passa" com dados quebrados; use `error` no crítico.
- Não testar a **chave** (unique+not_null) nem **relationships** — os erros mais caros.
- Escrever expectations/tests genéricos demais que nunca pegam nada.
- Não versionar as suítes/tests — qualidade vira conhecimento tribal.

## 💼 O que o mercado espera
Escrever testes de dados (dbt e/ou GE) e saber **onde** aplicá-los (fronteira vs consumo) é
esperado. Conhecer GE além do dbt mostra repertório — muitas vagas citam Great Expectations
nominalmente.

:::{admonition} ✨ Em resumo
:class: resumo
- Qualidade vira **teste automático**: dbt (`not_null/unique/accepted_values/relationships` + singulares) e **Great Expectations** (expectations + Data Docs).
- **dbt** para dados já no DW; **GE** para validar na **fronteira** (ingestão) e dados fora do dbt.
- Todo teste = **query que busca violações** (0 = passa).
- Times sérios usam os dois e barram falhas no CI.
:::

## 🧠 Quiz de recall
1. Cite os testes genéricos do dbt.
   :::{dropdown} Resposta
   not_null, unique, accepted_values, relationships (FK); regras de negócio viram testes singulares.
   :::
2. O que é o Great Expectations?
   :::{dropdown} Resposta
   Uma biblioteca de validação independente onde você declara expectations sobre um dataset (não-nulo, único, no conjunto, entre valores...), gerando um relatório (Data Docs) e falhando se não baterem.
   :::
3. Quando usar GE em vez de dbt tests?
   :::{dropdown} Resposta
   Para validar na fronteira (arquivo/carga recém-chegada, antes de gravar) e dados que não passam pelo dbt; dbt para dados já no DW transformados por ele.
   :::
4. O que todo teste de dados faz por baixo?
   :::{dropdown} Resposta
   Executa uma consulta que busca as linhas que violam a regra; 0 violações = passa.
   :::
5. Por que não deixar todos os testes como `warn`?
   :::{dropdown} Resposta
   Porque o build "passa" mesmo com dados quebrados; testes críticos devem ser `error` para barrar a carga/deploy.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "dbt tests ou Great Expectations?"
  :::{dropdown} Resposta modelo
  Depende de onde. GE na ingestão para validar dados crus na fronteira antes de gravar (e dados fora do dbt). dbt tests no DW para integridade dos models (unique/not_null/relationships) versionados junto do código. Em geral uso os dois e faço o CI barrar falhas.
  :::
- **P:** "Quais testes você nunca deixa de fazer?"
  :::{dropdown} Resposta modelo
  Chave da dimensão (unique + not_null) e integridade referencial (relationships) do fato para as dimensões — são os erros mais caros (duplicação e órfãos). Além de accepted_values em domínios e freshness.
  :::

## 🚀 Para ir além (leitura dirigida)
- **dbt docs** — *Tests* (genéricos e singulares).
- **Great Expectations docs** — *Expectations* e *Data Docs*.

## 📚 Referências
- dbt — Documentação oficial (testes de dados). <!-- @docs-dbt -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — qualidade e testes. <!-- @reis2022 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
