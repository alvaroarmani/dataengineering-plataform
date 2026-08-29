# Custos, otimização e panorama de DWs cloud

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Num DW cloud, **cada query tem um preço**. Um `SELECT *` distraído numa tabela de terabytes
pode custar caro — e a diferença entre um engenheiro júnior e um pleno muitas vezes é
**consciência de custo**: saber escrever consultas baratas e escolher a arquitetura certa.
Nesta unidade fechamos o M6 entendendo **como os DWs cloud cobram**, as alavancas de
otimização, e como BigQuery, Snowflake e Redshift se comparam.

## 💡 Conceito (o porquê)

### Os dois eixos de custo: armazenamento vs computação
Quase todo DW cloud separa **armazenamento** (guardar os dados, cobrado por GB/mês) de
**computação** (executar as queries). A grande diferença entre plataformas é **como cobram a
computação**:

- **Por bytes varridos** (BigQuery on-demand): você paga pelos dados que a query **lê**.
- **Por tempo de compute** (Snowflake, BigQuery editions/slots): você paga pelo **tempo** que
  um "warehouse"/slot fica ligado processando.

Entender qual modelo você está usando define as alavancas de otimização.

### Alavancas de otimização de custo
1. **Ler menos colunas** — o colunar cobra pelo que lê; `SELECT col1, col2` ≪ `SELECT *`.
2. **Ler menos linhas/partições** — filtre pela **coluna de partição** (pruning) e clusterize.
3. **Estimar antes (dry run)** — veja os bytes previstos antes de rodar.
4. **Cache de resultados** — resultados idênticos recentes podem sair de graça (BigQuery).
5. **Materialized views / tabelas agregadas** — pré-computam agregações caras e recorrentes.
6. **Expiração e storage frio** — dados não tocados há tempo custam menos (long-term storage);
   tabelas temporárias com expiração evitam armazenamento eterno.
7. **Auto-suspend** (Snowflake) — desligar o warehouse ocioso para não pagar compute à toa.

### Panorama: os principais DWs cloud
Todos separam storage/compute; diferem em operação e cobrança:

| Plataforma | Compute | Cobrança típica | Operação |
|---|---|---|---|
| **BigQuery** (Google) | serverless (slots) | por **bytes varridos** (on-demand) ou slots | mínima — sem cluster |
| **Snowflake** | *virtual warehouses* | por **segundo** de warehouse ligado (auto-suspend) | baixa — dimensiona warehouse |
| **Redshift** (AWS) | cluster provisionado (ou serverless) | por **nó/hora** (ou RPU) | maior — gerencia cluster |
| **Databricks SQL** | lakehouse sobre object store | por DBU/compute | média |

O fio comum: **separação storage/compute** e **elasticidade**. A escolha depende do ecossistema
(GCP/AWS/Azure), do modelo de custo que casa com seu uso e da tolerância a operação.

## 🔎 Exemplo
Uma tabela de 2 TB, 40 colunas, particionada por mês. A pergunta "receita de jan/2025 por
categoria":
- `SELECT *` sem filtro → varre ~2 TB → caro.
- `SELECT categoria, price ... WHERE mes = '2025-01'` → lê 2 colunas de 1 partição → varre
  poucos GB → **centenas de vezes mais barato**, mesmo resultado.
A diferença não é de correção — é de **custo e latência**. É isso que o dry run revela antes.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley descrevem a era dos DWs cloud como a separação de armazenamento e computação
com **elasticidade e cobrança por uso** — o que transfere a responsabilidade do engenheiro de
"dimensionar hardware" para "modelar bem e controlar o custo de consulta". BigQuery, Snowflake
e Redshift são as referências dessa geração. — *Fundamentals of Data Engineering*, cap. 6 e 8.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Times maduros tratam custo como métrica de engenharia: monitoram bytes varridos por query,
criam tabelas agregadas para dashboards recorrentes e barram `SELECT *` em revisão de código —
porque em on-demand o custo é diretamente proporcional aos bytes lidos. — BigQuery, docs (custos).
:::

## ⚠️ Erros comuns
- Não saber **qual modelo de cobrança** está usando (bytes vs tempo) — otimiza a alavanca errada.
- `SELECT *` e ausência de filtro de partição — o clássico "query cara".
- Recalcular a mesma agregação pesada toda hora em vez de uma **tabela agregada/MV**.
- Esquecer warehouses ligados (Snowflake) sem **auto-suspend** — paga compute ocioso.
- Escolher a plataforma por hype, não pelo **ecossistema e modelo de custo** do seu caso.

## 💼 O que o mercado espera
"Como você reduziria o custo desse pipeline/consulta?" é pergunta real de entrevista e de code
review. Conhecer o panorama (BigQuery/Snowflake/Redshift) e saber justificar trade-offs de
custo e operação diferencia candidatos plenos.

:::{admonition} ✨ Em resumo
:class: resumo
- Custo em DW cloud tem dois eixos: **armazenamento** (GB/mês) e **computação** (bytes varridos
  **ou** tempo de warehouse).
- Alavancas: menos colunas, menos partições, dry run, cache, materialized views, expiração, auto-suspend.
- BigQuery (serverless/bytes), Snowflake (warehouses/tempo), Redshift (cluster/nó-hora) — todos
  **separam storage/compute**.
- Consciência de custo é habilidade de engenharia, não detalhe.
:::

## 🧠 Quiz de recall
1. Quais são os dois eixos de custo de um DW cloud?
   :::{dropdown} Resposta
   Armazenamento (guardar os dados, por GB/mês) e computação (executar queries — cobrada por bytes varridos ou por tempo de warehouse).
   :::
2. Diferença entre cobrar "por bytes varridos" e "por tempo de compute"?
   :::{dropdown} Resposta
   Por bytes (BigQuery on-demand): paga pelos dados lidos pela query. Por tempo (Snowflake): paga pelos segundos que o warehouse fica ligado processando, independente dos bytes.
   :::
3. Cite quatro alavancas de otimização de custo.
   :::{dropdown} Resposta
   Ler menos colunas (sem SELECT *), filtrar pela coluna de partição (pruning), usar cache de resultados, materialized views/tabelas agregadas; também dry run, expiração e auto-suspend.
   :::
4. O que BigQuery, Snowflake e Redshift têm em comum?
   :::{dropdown} Resposta
   Todos separam armazenamento de computação e oferecem elasticidade/cobrança por uso; diferem em como cobram o compute e no nível de operação.
   :::
5. Por que uma tabela agregada/materialized view reduz custo?
   :::{dropdown} Resposta
   Pré-computa uma agregação cara e recorrente uma vez, evitando varrer a tabela grande toda vez que o dashboard/consulta roda.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Um dashboard roda a mesma agregação pesada o dia todo e está caro. O que você faz?"
  :::{dropdown} Resposta modelo
  Materializo a agregação numa tabela/MV atualizada em cadência (ex.: de hora em hora), e aponto o dashboard para ela. Assim a query cara roda uma vez por atualização, não a cada visita, cortando bytes varridos/compute drasticamente.
  :::
- **P:** "Como escolher entre BigQuery e Snowflake?"
  :::{dropdown} Resposta modelo
  Olho ecossistema (GCP vs multi-cloud), o padrão de uso (picos esporádicos favorecem o on-demand por bytes do BigQuery; uso contínuo e previsível pode favorecer warehouses do Snowflake com auto-suspend), e o apetite por operação. Ambos separam storage/compute; a decisão é de custo e integração, não de "qual é melhor".
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering**, cap. 6 e 8 (DW cloud, storage/serving, custo).
- **BigQuery docs** — *Controlling costs* e *Best practices for query performance*.

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — cap. 6 e 8 (DW cloud, custo). <!-- @reis2022 -->
- BigQuery — Documentação oficial (controle de custos, boas práticas de consulta). <!-- @docs-bigquery -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — cap. 3 (armazenamento e custo de leitura). <!-- @kleppmann2017 -->

*Acessado em: 2026-08-24.*

---
**Revisado em:** 2026-08-24
