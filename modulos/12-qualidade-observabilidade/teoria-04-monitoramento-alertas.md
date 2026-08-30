# Monitoramento, alertas e cultura de confiabilidade

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Detectar um problema (U3) só vale se **alguém for avisado, no canal certo, sem afogar em
ruído**. Alertas demais viram *alert fatigue* (todo mundo ignora); de menos, e o problema passa.
Fechar o ciclo — **medir → alertar → responder → melhorar** — é o que cria uma **cultura de
confiabilidade** nos dados. Esta unidade fecha o M12 conectando qualidade/observabilidade à
operação.

## 💡 Conceito (o porquê)

### Severidade e o alerta certo
Nem todo problema é urgente. Classifique:
- **error/crítico:** barra a carga/deploy e **acorda alguém** (ex.: chave duplicada, tabela stale
  além do SLA). 
- **warn/aviso:** registra e notifica sem bloquear (ex.: 3% de nulos numa coluna tolerante).
O alerta vai ao **canal certo** (Slack/e-mail/PagerDuty) com **contexto** (o que, onde, quando,
link para o log/lineage).

### Evitar alert fatigue
- **Só alerte no acionável:** se ninguém faz nada com o alerta, ele não deveria existir.
- **Agrupe/deduplique:** um incidente = um alerta, não 500.
- **Limiares calibrados:** muito sensível gera ruído; ajuste com o histórico.
- **Runbook:** cada alerta aponta "o que fazer" — reduz o tempo de resposta.

### SLIs, SLOs e o ciclo de confiabilidade
Empreste do SRE:
- **SLI** (indicador): a métrica (ex.: % de cargas dentro do SLA de freshness).
- **SLO** (objetivo): a meta (ex.: 99% das cargas frescas no mês).
- Quando o SLO é ameaçado, prioriza-se a correção. Fecha o ciclo **medir → alertar → responder
  (com runbook) → post-mortem → melhorar**.

### Post-mortem sem culpa
Após um incidente de dados, um **post-mortem** (o que houve, impacto, causa raiz, ação
preventiva) — **sem culpar pessoas** — transforma o erro em melhoria do sistema. É o que
distingue times que aprendem.

## 🔎 Exemplo
Monitor de freshness marca `vendas` stale (SLA 24h estourado) → alerta **error** no Slack do
time com link para o run do Airflow (M9) e o lineage (U3). O runbook diz: "verificar a API a
montante; se caiu, reprocessar com backfill (idempotente, M9)". Resolvido, um post-mortem curto
vira um novo teste/monitor para não repetir.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley conectam observabilidade a **confiabilidade operacional**: alertas acionáveis,
SLAs/SLOs e post-mortems sem culpa formam a cultura que mantém a confiança nos dados — o oposto
do "descobrir pelo chefe". — *Fundamentals of Data Engineering* (confiabilidade).
:::

:::{admonition} 🏭 Do mundo real
:class: important
Times de dados adotam práticas de SRE: severidade nos alertas, canais certos, runbooks e
post-mortems sem culpa. O maior inimigo é o **alert fatigue** — por isso "só alerte no
acionável" é regra de ouro. — Reis & Housley.
:::

## ⚠️ Erros comuns
- **Alertas demais** (não acionáveis) → todo mundo ignora (*alert fatigue*).
- Alertar no **canal errado** ou sem **contexto/runbook** → resposta lenta.
- Tratar tudo como **crítico** (ou nada) → sem priorização real.
- Não medir **SLI/SLO** → "confiabilidade" vira achismo.
- Post-mortem com **culpa** → as pessoas escondem erros; o sistema não melhora.

## 💼 O que o mercado espera
Saber desenhar alertas por **severidade**, evitar fatigue, e falar de **SLA/SLO/runbook/
post-mortem** mostra maturidade operacional — cada vez mais pedida (a fronteira entre DE e
"data reliability engineering").

:::{admonition} ✨ Em resumo
:class: resumo
- Alerte por **severidade** (error acorda/bloqueia; warn notifica), no **canal certo** e com **contexto/runbook**.
- Combata **alert fatigue**: só alerte no **acionável**, agrupe, calibre limiares.
- Use **SLI/SLO** para medir confiabilidade; feche o ciclo **medir→alertar→responder→melhorar**.
- **Post-mortem sem culpa** transforma incidente em melhoria do sistema.
:::

## 🧠 Quiz de recall
1. Diferença entre alerta error e warn?
   :::{dropdown} Resposta
   error é crítico (bloqueia a carga/deploy e aciona alguém); warn notifica/registra sem bloquear. A severidade define a resposta.
   :::
2. O que é alert fatigue e como evitar?
   :::{dropdown} Resposta
   Excesso de alertas (não acionáveis) que leva todos a ignorá-los. Evita-se alertando só no acionável, agrupando/deduplicando e calibrando limiares.
   :::
3. O que são SLI e SLO?
   :::{dropdown} Resposta
   SLI é o indicador medido (ex.: % de cargas dentro do SLA de freshness); SLO é a meta (ex.: 99% no mês). Emprestados do SRE.
   :::
4. Para que serve um runbook?
   :::{dropdown} Resposta
   Dizer "o que fazer" quando o alerta dispara — reduz o tempo de resposta e padroniza a correção.
   :::
5. Por que post-mortem sem culpa?
   :::{dropdown} Resposta
   Para as pessoas relatarem erros honestamente e o foco ficar na causa raiz/prevenção (melhorar o sistema), não em punir.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você evita que seu time ignore os alertas?"
  :::{dropdown} Resposta modelo
  Alertando só no acionável (se ninguém age, não é alerta), classificando por severidade, agrupando por incidente, calibrando limiares com o histórico e anexando runbook/contexto. Alertas raros e úteis são respeitados; ruído gera alert fatigue.
  :::
- **P:** "Como você mede a confiabilidade de um pipeline?"
  :::{dropdown} Resposta modelo
  Com SLIs/SLOs: defino indicadores (freshness dentro do SLA, taxa de testes passando, volume estável) e metas (ex.: 99% de cargas frescas/mês). Monitoro, alerto quando o SLO é ameaçado e faço post-mortem sem culpa após incidentes para melhorar.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (confiabilidade, SLAs, post-mortem).
- **Google SRE Book** (SLI/SLO, alerting, post-mortem sem culpa) — conceitos transferíveis.

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — confiabilidade e alertas. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — monitoramento e resposta. <!-- @densmore2021 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — confiabilidade operacional. <!-- @kleppmann2017 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
