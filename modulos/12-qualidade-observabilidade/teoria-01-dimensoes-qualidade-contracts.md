# Dimensões de qualidade de dados e data contracts

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Pipelines que "rodam sem erro" ainda entregam **dados errados** — e um número errado num
dashboard custa decisões erradas e **confiança**. Qualidade de dados não é achismo: tem
**dimensões mensuráveis**. E, para não descobrir o problema tarde, times firmam **data
contracts** — acordos explícitos sobre o formato/semântica dos dados entre quem produz e quem
consome. Esta unidade dá o vocabulário para medir e garantir qualidade.

## 💡 Conceito (o porquê)

### As dimensões de qualidade
Medimos qualidade por dimensões (cada uma vira um teste, U2):
- **Completude:** faltam valores? (% de nulos numa coluna que deveria ser preenchida).
- **Unicidade:** há duplicatas onde a chave deveria ser única?
- **Validade:** os valores respeitam o domínio/tipo? (ex.: `status ∈ {pago, cancelado}`; data válida).
- **Consistência:** os dados batem entre si e entre fontes? (o total do fato = soma das partes; FK existe).
- **Atualidade (freshness):** os dados estão recentes o bastante? (chegaram hoje?).
- **Acurácia:** refletem a realidade? (a mais difícil de medir automaticamente).

### Data contract
Um **data contract** é um **acordo explícito** entre produtor e consumidor sobre um dataset:
schema (campos e tipos), semântica, garantias de qualidade (ex.: `pedido_id` único e não-nulo),
e frequência/freshness. Formaliza o que antes era implícito ("achei que essa coluna nunca era
nula"). Quando o produtor quebra o contrato, a checagem **falha cedo** — antes de contaminar o
consumidor.

### Por que contratos importam
Sem contrato, uma mudança inocente na origem (renomear coluna, mudar tipo, parar de preencher)
quebra silenciosamente relatórios lá na frente. O contrato torna a expectativa **testável** e
desloca a falha para **perto da origem** (shift-left), onde é barata de corrigir.

## 🔎 Exemplo
Contrato de `pedidos`: `pedido_id` (int, único, not null), `status` ∈ {pago, cancelado,
enviado}, `valor` ≥ 0, atualizado diariamente. Uma carga que traz `pedido_id` duplicado
(unicidade) ou `status='X'` (validade) **falha o contrato** e é barrada — em vez de inflar o
fato e aparecer como número errado no dashboard de vendas dias depois.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley tratam **qualidade de dados** como *undercurrent*: dados sem qualidade medida são
dados em que ninguém confia. Densmore detalha checagens de completude, unicidade, validade e
consistência como parte esperada de pipelines confiáveis. — *Fundamentals of Data Engineering*;
*Data Pipelines Pocket Reference*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
**Data contracts** viraram prática de times maduros: o produtor declara garantias (schema +
qualidade + freshness) e o pipeline as valida na fronteira, deslocando a detecção de problemas
para perto da origem (shift-left) — evitando "data downtime". — Reis & Housley (qualidade).
:::

## ⚠️ Erros comuns
- Confundir "**rodou sem erro**" com "**dados corretos**" — sucesso técnico ≠ qualidade.
- Não medir **unicidade da chave** — duplicatas inflam agregações a jusante.
- Ignorar **freshness** — o pipeline "passa" com dados velhos.
- Expectativas **implícitas** (sem contrato) — quebram em silêncio quando a origem muda.
- Testar só no fim (consumo) em vez de **na fronteira** (perto da origem).

## 💼 O que o mercado espera
Saber nomear as dimensões de qualidade e o que é um data contract — e por que "shift-left" — é
esperado de quem cuida de pipelines. "Como você garante a qualidade dos dados?" é pergunta
recorrente; a resposta passa por dimensões mensuráveis + contratos + testes (U2).

:::{admonition} ✨ Em resumo
:class: resumo
- Qualidade tem **dimensões mensuráveis**: completude, unicidade, validade, consistência, freshness, acurácia.
- **Data contract** = acordo explícito (schema + semântica + garantias + freshness) entre produtor e consumidor.
- Contratos tornam expectativas **testáveis** e deslocam a falha para perto da origem (**shift-left**).
- "Rodou sem erro" ≠ "dados corretos".
:::

## 🧠 Quiz de recall
1. Cite quatro dimensões de qualidade de dados.
   :::{dropdown} Resposta
   Completude, unicidade, validade, consistência (também freshness/atualidade e acurácia).
   :::
2. O que é um data contract?
   :::{dropdown} Resposta
   Um acordo explícito entre produtor e consumidor sobre um dataset: schema, semântica, garantias de qualidade e freshness — tornando as expectativas testáveis.
   :::
3. O que significa "shift-left" em qualidade?
   :::{dropdown} Resposta
   Deslocar a detecção de problemas para perto da origem (na fronteira de entrada), onde são baratos de corrigir, em vez de descobrir no consumo.
   :::
4. Por que "rodou sem erro" não basta?
   :::{dropdown} Resposta
   Porque o pipeline pode completar tecnicamente e ainda entregar dados errados (duplicados, nulos, fora do domínio, velhos) — qualidade precisa ser medida.
   :::
5. Como a unicidade afeta agregações?
   :::{dropdown} Resposta
   Chaves duplicadas inflam somas/contagens no join com o fato — números errados a jusante.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você garante a qualidade dos dados de um pipeline?"
  :::{dropdown} Resposta modelo
  Defino as dimensões que importam (completude, unicidade da chave, validade de domínio, consistência, freshness) e as transformo em testes que rodam na fronteira (shift-left). Formalizo as expectativas num data contract com o produtor, e barro cargas que violam o contrato antes de contaminar o consumo.
  :::
- **P:** "O que é um data contract e o que ele evita?"
  :::{dropdown} Resposta modelo
  Um acordo explícito sobre schema, semântica, qualidade e freshness de um dataset. Evita quebras silenciosas: quando a origem muda (renomeia coluna, muda tipo, para de preencher), a checagem do contrato falha cedo, perto da origem, em vez de aparecer como número errado no dashboard.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (qualidade de dados, undercurrents).
- **Densmore — Data Pipelines Pocket Reference** (checagens de qualidade).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — qualidade de dados. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — validação e confiabilidade. <!-- @densmore2021 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — integridade e confiabilidade. <!-- @kleppmann2017 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
