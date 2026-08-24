# Slowly Changing Dimensions (SCD): versionando o histórico

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Uma cliente morava em São Paulo quando fez a compra do ano passado; hoje mora em Campinas.
Se você **simplesmente atualizar** a cidade dela na dimensão, todas as vendas antigas passam
a "ter acontecido" em Campinas — e o relatório de receita por cidade do ano passado muda
sozinho. Dimensões mudam com o tempo (cliente muda de cidade, produto muda de categoria), e
**como** você lida com essa mudança define se o seu histórico continua correto. Kimball deu
nome a essas estratégias: as **Slowly Changing Dimensions** (SCDs).

## 💡 Conceito (o porquê)

Uma SCD é uma **política** para tratar mudanças nos atributos de uma dimensão. Os tipos mais
usados:

### Tipo 0 — reter o original
O atributo **nunca muda** depois de gravado (ex.: data de nascimento, data original do
cadastro). Simples: ignora qualquer mudança da origem.

### Tipo 1 — sobrescrever (sem histórico)
**Atualiza no lugar**: o valor novo apaga o antigo. Não guarda histórico. Bom para
**correções** (o CEP estava digitado errado) — você não quer "preservar" um erro. Ruim quando
o histórico importa, porque reescreve o passado.

### Tipo 2 — nova linha (histórico completo) ⭐
A estratégia mais importante. Em vez de sobrescrever, você **insere uma nova linha** com a
versão nova e **encerra** a linha antiga. A mesma entidade (mesma **chave natural**) passa a
ter **várias linhas**, cada uma com sua **surrogate key** — por isso o SCD2 depende de
surrogate keys (unidade anterior). Colunas de controle típicas:

- **`valido_de` / `valido_ate`**: o intervalo em que aquela versão vigorou.
- **`corrente`** (flag booleana): marca a linha vigente hoje.

O fato aponta para a **surrogate key da versão vigente na hora do evento** — então uma venda
antiga continua ligada à "São Paulo" de então, e o histórico permanece correto.

### Tipo 3 — nova coluna (histórico limitado)
Guarda **o valor anterior numa coluna extra** (ex.: `cidade_atual` e `cidade_anterior`).
Mantém só **uma** mudança anterior — útil em casos raros (ex.: reorganização de território em
que você quer comparar "antes/depois"), não para histórico completo.

### Como consultar uma SCD2
Duas perguntas clássicas:
- **Visão atual:** `WHERE corrente = TRUE` — o estado de hoje.
- **Point-in-time** (como era numa data): `WHERE valido_de <= :data AND :data < valido_ate` —
  recupera a versão vigente naquela data.

## 🔎 Exemplo

Ana (chave natural `cliente_id = 100`) muda de São Paulo para Campinas em 01/03/2025:

| sk | cliente_id | cidade | valido_de | valido_ate | corrente |
|----|-----------|--------|-----------|-----------|----------|
| 1 | 100 | São Paulo | 2024-01-01 | 2025-03-01 | false |
| 2 | 100 | Campinas | 2025-03-01 | 9999-12-31 | true |

A venda de Ana em 2024 aponta para `sk = 1` (São Paulo); a de hoje, para `sk = 2` (Campinas).
O relatório histórico continua certo — nada do passado foi reescrito.

:::{admonition} 📖 Da literatura
:class: seealso
Kimball trata as SCDs como técnica central da modelagem dimensional e descreve o **Tipo 2**
como a resposta padrão quando o histórico precisa ser preservado: uma nova linha por versão,
com surrogate key própria e colunas de vigência (datas efetivas e um indicador de linha
corrente). — *The Data Warehouse Toolkit*, cap. 5 (SCDs).
:::

:::{admonition} 🏭 Do mundo real
:class: important
Densmore observa que, na prática de pipelines, a lógica de SCD2 costuma virar um passo de
*merge/upsert* na carga da dimensão: comparar o registro que chegou com a linha corrente,
e — se algo mudou — encerrar a corrente e inserir a nova. Ferramentas como o dbt oferecem
isso pronto (snapshots). — *Data Pipelines Pocket Reference*.
:::

## ⚠️ Erros comuns
- **Usar Tipo 1 onde o histórico importa** — reescreve o passado e "estraga" relatórios antigos.
- **Fazer SCD2 sem surrogate key** — impossível ter várias versões da mesma chave natural.
- **Esquecer de encerrar a linha antiga** (`valido_ate`/`corrente`) — gera duas linhas "correntes" e duplica no fato.
- **Intervalos que se sobrepõem** em `valido_de`/`valido_ate` — o point-in-time passa a retornar mais de uma versão.
- Aplicar SCD2 a **todos** os atributos por reflexo — versione só o que o negócio precisa acompanhar.

## 💼 O que o mercado espera
"Explique SCD Tipo 1 vs Tipo 2" é das perguntas mais frequentes em entrevistas de
Analytics/Data Engineer. No trabalho, você vai configurar **snapshots do dbt** (M07) ou
escrever o *merge* de SCD2 na carga — e justificar quando cada tipo se aplica.

:::{admonition} ✨ Em resumo
:class: resumo
- SCD = política para mudanças em dimensões. **Tipo 1** sobrescreve (sem histórico);
  **Tipo 2** cria nova linha (histórico completo); **Tipo 3** guarda o valor anterior numa coluna.
- **Tipo 2** é o padrão para preservar histórico e **depende de surrogate keys** + colunas
  `valido_de`/`valido_ate`/`corrente`.
- Consultas típicas: **atual** (`corrente = TRUE`) e **point-in-time** (intervalo de vigência).
- O fato aponta para a **versão vigente no momento do evento** — o passado nunca é reescrito.
:::

## 🧠 Quiz de recall
1. O que é uma Slowly Changing Dimension?
   :::{dropdown} Resposta
   Uma política para tratar mudanças nos atributos de uma dimensão ao longo do tempo (ex.: cliente muda de cidade), preservando — ou não — o histórico conforme o tipo.
   :::
2. Diferença entre SCD Tipo 1 e Tipo 2?
   :::{dropdown} Resposta
   Tipo 1 sobrescreve o valor (sem histórico); Tipo 2 insere uma nova linha para a versão nova e encerra a antiga (histórico completo, com surrogate keys e colunas de vigência).
   :::
3. Por que o SCD2 depende de surrogate keys?
   :::{dropdown} Resposta
   Porque a mesma entidade (mesma chave natural) passa a ter várias linhas/versões; só a surrogate key (única por linha) distingue cada versão e permite o fato apontar para a certa.
   :::
4. Quais colunas de controle são típicas no SCD2?
   :::{dropdown} Resposta
   `valido_de` e `valido_ate` (intervalo de vigência) e uma flag `corrente` indicando a linha vigente hoje.
   :::
5. Como recuperar a versão de um cliente vigente numa data específica (point-in-time)?
   :::{dropdown} Resposta
   `WHERE valido_de <= :data AND :data < valido_ate` — retorna a versão que vigorava naquela data.
   :::
6. Quando o Tipo 1 é a escolha certa?
   :::{dropdown} Resposta
   Para correções de erro (ex.: um dado digitado errado), quando não faz sentido preservar o valor incorreto no histórico.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Um cliente mudou de cidade. Como seu modelo lida com isso sem estragar os relatórios antigos?"
  :::{dropdown} Resposta modelo
  Uso SCD Tipo 2: em vez de sobrescrever, encerro a linha corrente (`valido_ate` = data da mudança, `corrente = false`) e insiro uma nova linha com a cidade nova, nova surrogate key e `corrente = true`. As vendas antigas continuam apontando para a surrogate da versão de então, então o histórico por cidade permanece correto.
  :::
- **P:** "Quando você usaria Tipo 1 em vez de Tipo 2?"
  :::{dropdown} Resposta modelo
  Tipo 1 para correções, onde preservar o valor antigo não agrega (um CEP digitado errado, por exemplo). Tipo 2 quando o negócio precisa analisar o passado como ele era. Muitas dimensões misturam: alguns atributos Tipo 1, outros Tipo 2.
  :::
- **P:** "Como você evita duas linhas 'correntes' para o mesmo cliente?"
  :::{dropdown} Resposta modelo
  A carga da dimensão é um merge/upsert transacional: ao detectar mudança, primeiro encerro a linha corrente (seto `valido_ate` e `corrente=false`) e só então insiro a nova como corrente. Garanto também que os intervalos `valido_de`/`valido_ate` não se sobreponham.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kimball & Ross — The Data Warehouse Toolkit**, cap. 5 (os tipos de SCD em detalhe).
- **dbt docs — Snapshots** (implementação prática de SCD2 no dia a dia).

## 📚 Referências
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit*, 3ª ed. (2013) — cap. 5 (SCDs). <!-- @kimball2013 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — carga de dimensões / SCD. <!-- @densmore2021 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 8 (modelagem para consumo). <!-- @reis2022 -->
- dbt — Documentação oficial (Snapshots). <!-- @docs-dbt -->

*Acessado em: 2026-08-23.*

---
**Revisado em:** 2026-08-23
