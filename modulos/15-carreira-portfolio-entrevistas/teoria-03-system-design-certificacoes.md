# System design de pipeline de dados e trilha de certificações

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Nas entrevistas de pleno/sênior aparece uma prova mais aberta: **"desenhe um pipeline para X"** —
sem resposta única, avaliando como você **arquiteta um sistema de dados** sob requisitos e
restrições. É a prova que mais assusta porque não se decora; ela integra tudo do curso (ingestão,
dbt, Airflow, DW, qualidade, governança). Somado a isso, muitos candidatos se perguntam **quais
certificações valem a pena**. Este módulo dá um **framework para conduzir o system design** e uma
leitura honesta do papel das certificações.

## 💡 Conceito (o porquê)

### System design de dados: um roteiro
Diante de "projete um pipeline para o app de delivery reportar vendas por região a cada hora",
conduza assim:
1. **Requisitos primeiro.** Volume (linhas/dia), **latência** (tempo real ou batch horário?),
   **freshness**, consumidores (dashboard? ML?), orçamento. Sem isso você projeta no vácuo.
2. **Batch vs streaming.** A latência exigida decide. "A cada hora" → **batch** é suficiente e mais
   simples/barato; "reagir em segundos" → streaming. Escolher streaming sem necessidade é
   over-engineering.
3. **Desenhe as camadas** (o ciclo de vida do dado): **ingestão** (de onde, como, incremental?) →
   **armazenamento** (data lake/warehouse) → **transformação** (ELT com dbt: staging→marts) →
   **serving** (o dashboard). Um diagrama simples > mil palavras.
4. **Orquestração e agendamento** (Airflow: dependências, retries, backfill).
5. **As *undercurrents*** (o que separa júnior de pleno): **qualidade** (testes/contratos),
   **idempotência** (reprocessar sem duplicar), **observabilidade** (e se falhar às 3h?),
   **segurança/governança/custo**. Mencioná-las mostra maturidade.
6. **Trade-offs explícitos.** Não existe "certo": existe "adequado aos requisitos". Diga o que
   você escolheu **e o que abriu mão**.

### Por que "requisitos primeiro" é a chave
O erro nº 1 é sair citando ferramentas ("uso Kafka, Spark, Snowflake") antes de entender o
problema. O entrevistador quer ver **julgamento**: a solução mais simples que atende os requisitos
vence. Ferramenta é consequência do requisito, nunca o ponto de partida.

### Certificações: úteis, mas não substituem portfólio
Certificações **complementam**, não substituem, projetos reais. Elas ajudam a: passar em filtros
de RH, dar estrutura ao estudo e sinalizar comprometimento — mas nenhuma prova que você **constrói**
como um repositório com pipeline rodando. Ordem de prioridade para migração de carreira:
**portfólio + TCC primeiro**; certificação depois, escolhida pela stack da vaga-alvo. As mais
reconhecidas na área: **dbt Analytics Engineering**, **Astronomer Airflow**, e as de cloud
(**Google Professional Data Engineer**, AWS/Azure equivalentes). Escolha **uma** alinhada ao seu
foco, não uma coleção.

### O DE é engenharia de software aplicada a dados
Todo o system design reforça a tese do curso: o engenheiro de dados pensa em **sistemas** —
confiabilidade, escalabilidade, manutenção — não em scripts isolados. É por isso que Git, testes,
CI e arquitetura pesam tanto quanto SQL.

## 🔎 Exemplo
"Projete o pipeline de vendas horárias." Você responde: "Primeiro, requisitos: latência de 1h →
**batch**; volume moderado → não preciso de Spark. Ingestão: extrair incremental do banco do app
para um data lake (só o que mudou). Transformação: **dbt** (staging → fato_vendas + dim_regiao).
Orquestração: **Airflow**, DAG horária com retries e idempotência (recarga por partição de hora).
Serving: o dashboard lê os marts. Undercurrents: testes dbt (not_null/unique), alerta se a DAG
falhar, controle de custo por consultar só a partição do dia. Trade-off: batch horário troca
tempo-real por simplicidade e custo — adequado ao requisito." Isso é um system design de nível
pleno.

:::{admonition} 📖 Da literatura
:class: seealso
Kleppmann estrutura o design de sistemas de dados em torno de **confiabilidade, escalabilidade e
manutenibilidade**, e do contraste batch vs stream — o vocabulário exato do system design. Reis &
Housley enquadram o pipeline pelo **ciclo de vida do dado** e pelas *undercurrents* que decidem a
maturidade da solução. — *Designing Data-Intensive Applications*; *Fundamentals of Data
Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Candidatos são reprovados no system design menos por "não saber a ferramenta" e mais por **pular os
requisitos** e propor arquitetura complexa demais. Começar por latência/volume/consumidores e
justificar a escolha mais simples que atende é o que sinaliza senioridade. — prática de mercado;
Kleppmann.
:::

## ⚠️ Erros comuns
- **Citar ferramentas antes dos requisitos** — solução no vácuo.
- **Over-engineering** — streaming/Spark/Kafka sem necessidade real.
- **Ignorar as *undercurrents*** — nada de qualidade, idempotência, falhas ou custo.
- **Não desenhar** — descrever em prosa o que um diagrama resolveria.
- **Achar que certificação substitui portfólio** — ela complementa; projeto prova.

## 💼 O que o mercado espera
Conduzir um system design partindo dos requisitos, desenhar as camadas do pipeline, escolher batch
ou streaming com justificativa e citar as *undercurrents* (qualidade, idempotência, observabilidade,
custo). Sobre certificação: saber priorizar portfólio e escolher uma alinhada à vaga.

:::{admonition} ✨ Em resumo
:class: resumo
- **Requisitos primeiro** (volume, latência, consumidores, custo) — ferramenta vem depois.
- **Batch vs streaming** decidido pela latência; a solução mais simples que atende vence.
- Desenhe as **camadas** (ingestão→armazenamento→transformação→serving) + orquestração + **undercurrents**.
- **Certificação complementa, não substitui** o portfólio; escolha uma alinhada ao foco.
:::

## 🧠 Quiz de recall
1. Qual é o primeiro passo de um system design de dados?
   :::{dropdown} Resposta
   Levantar os requisitos: volume, latência/freshness, consumidores e orçamento — antes de pensar em ferramentas.
   :::
2. O que decide entre batch e streaming?
   :::{dropdown} Resposta
   A latência exigida: se dá para atualizar em janelas (ex.: horário), batch basta e é mais simples/barato; segundos de reação pedem streaming.
   :::
3. O que são as *undercurrents* e por que mencioná-las?
   :::{dropdown} Resposta
   Qualidade, segurança, gestão de dados, DataOps, arquitetura e orquestração que permeiam todo o pipeline; citá-las mostra maturidade além do "caminho feliz".
   :::
4. Por que over-engineering é um erro no system design?
   :::{dropdown} Resposta
   Porque adiciona complexidade e custo sem atender melhor os requisitos; o julgamento avaliado é escolher a solução mais simples que resolve.
   :::
5. Certificação substitui portfólio? Por quê?
   :::{dropdown} Resposta
   Não; ela complementa (filtros de RH, estrutura de estudo, sinalização), mas só o portfólio prova que você constrói. Priorize projetos e escolha uma certificação alinhada à vaga.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Projete um pipeline para calcular receita diária de um e-commerce."
  :::{dropdown} Resposta modelo
  Requisitos: diário → batch; volume moderado. Ingestão incremental do banco → data lake; transformação em dbt (staging → fato_vendas, dimensões); orquestração Airflow (DAG diária, retries, idempotência por partição de dia); serving no dashboard/BI. Undercurrents: testes dbt, alerta de falha, custo controlado. Trade-off: batch diário troca tempo-real por simplicidade — adequado ao pedido. Desenho as camadas num diagrama.
  :::
- **P:** "Vale a pena tirar a certificação Google Professional Data Engineer?"
  :::{dropdown} Resposta modelo
  Depende do foco: se miro vagas GCP, ela ajuda em filtros e organiza o estudo. Mas priorizo o portfólio — um DW com dbt/Airflow rodando prova mais do que a prova. Faria a certificação depois do TCC, escolhendo a que casa com a stack das vagas que persigo, e apenas uma.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Kleppmann — Designing Data-Intensive Applications** (confiabilidade/escalabilidade, batch vs stream).
- **Reis & Housley — Fundamentals of Data Engineering** (ciclo de vida e *undercurrents*).
- **Densmore — Data Pipelines Pocket Reference** (padrões de pipeline para o desenho).

## 📚 Referências
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — design de sistemas de dados. <!-- @kleppmann2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — ciclo de vida e undercurrents. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — padrões de pipeline. <!-- @densmore2021 -->

*Acessado em: 2026-08-30.*

---
**Revisado em:** 2026-08-30
