# Observabilidade de dados: freshness, volume e anomalias

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Testes (U2) pegam violações que você **previu**. Mas e o que você não previu — a carga que
parou de chegar, o volume que despencou pela metade, um valor que saiu do padrão? Isso é
**observabilidade de dados**: instrumentar o pipeline para **detectar problemas** que nenhum
teste específico cobriria, reduzindo o **data downtime** (tempo em que os dados estão errados
ou indisponíveis sem ninguém saber).

## 💡 Conceito (o porquê)

### Os pilares da observabilidade de dados
Métricas que você monitora continuamente:
- **Freshness (atualidade):** quando o dado foi atualizado pela última vez? Passou do SLA
  (ex.: "deveria chegar todo dia às 6h")?
- **Volume:** quantas linhas chegaram? Uma queda/pico súbito vs o histórico sinaliza problema
  (fonte quebrou, duplicação).
- **Schema:** a estrutura mudou (coluna sumiu, tipo mudou)? — quebra a jusante.
- **Distribuição/valores:** as estatísticas (média, % de nulos, cardinalidade) fugiram do
  padrão? Um `NULL` explodindo ou uma média que dobrou é uma **anomalia**.
- **Lineage:** se algo quebrou, o que a montante causou e o que a jusante é afetado?

### Freshness na prática
Compara-se a **última atualização** com **agora** contra um **SLA**. Ex.: se a maior `data` da
tabela é de 2 dias atrás e o SLA é 24h, a tabela está **stale** → alerta. É o `source
freshness` do dbt e o coração de qualquer monitor de pipeline.

### Detecção de anomalias
Duas abordagens:
- **Regras/limiares:** "volume não pode cair mais de 30% vs a média dos últimos 7 dias";
  "nulos não passam de 5%". Simples e transparente.
- **Estatística/ML:** aprende a faixa normal (ex.: média ± k·desvio) e alerta fora dela. Mais
  poderoso, menos transparente. Comece pelas regras.

### Data downtime
É o tempo em que os dados estão errados/ausentes. Observabilidade **reduz o tempo de detecção**
(você descobre por um alerta, não pelo chefe) e **de resolução** (lineage aponta a causa).

## 🔎 Exemplo
A tabela `vendas` deveria receber ~10 mil linhas/dia. Hoje chegaram 400 (freshness OK, mas
**volume anômalo** −96%) → alerta automático. O time investiga pelo **lineage** e acha uma API
a montante que mudou de schema. Sem observabilidade, isso só apareceria quando o dashboard de
vendas ficasse estranho — dias e uma reunião depois.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley colocam **observabilidade** entre as *undercurrents*: além de testes, é preciso
monitorar freshness, volume e distribuição para detectar o inesperado e reduzir o **data
downtime** — o tempo em que os dados estão errados sem ninguém saber. — *Fundamentals of Data
Engineering* (observabilidade/confiabilidade).
:::

:::{admonition} 🏭 Do mundo real
:class: important
Ferramentas de *data observability* monitoram automaticamente freshness, volume, schema e
distribuição, alertando em anomalias — mas você chega longe com regras simples (SLA de
freshness, limiar de variação de volume, % de nulos) versionadas no próprio pipeline. —
Reis & Housley.
:::

## ⚠️ Erros comuns
- Só ter **testes** (o previsto) e nenhuma **observabilidade** (o inesperado).
- Não monitorar **freshness** — o pior silêncio é o dado que parou de chegar.
- Ignorar **volume** — quedas/picos denunciam fontes quebradas e duplicação.
- Partir para **ML de anomalia** antes de regras simples — comece por limiares transparentes.
- Sem **lineage**, o tempo de resolução dispara (não se acha a causa).

## 💼 O que o mercado espera
Conhecer os pilares (freshness, volume, schema, distribuição, lineage) e saber montar um monitor
simples (SLA de freshness, limiar de volume) é diferencial. "Como você saberia que um pipeline
quebrou?" é pergunta de maturidade.

:::{admonition} ✨ Em resumo
:class: resumo
- **Observabilidade** detecta o **inesperado** (o que os testes não previram), reduzindo o **data downtime**.
- Pilares: **freshness**, **volume**, **schema**, **distribuição/valores**, **lineage**.
- **Freshness** = última atualização vs agora contra um SLA; **anomalia** = fora do padrão (regra ou estatística).
- Comece por **regras/limiares** simples e transparentes.
:::

## 🧠 Quiz de recall
1. Qual a diferença entre testes e observabilidade?
   :::{dropdown} Resposta
   Testes checam violações previstas (regras específicas); observabilidade monitora sinais (freshness, volume, distribuição) para detectar o inesperado.
   :::
2. Como se mede freshness?
   :::{dropdown} Resposta
   Comparando a última atualização do dado com "agora" contra um SLA (ex.: deveria ter chegado nas últimas 24h).
   :::
3. Cite os pilares da observabilidade de dados.
   :::{dropdown} Resposta
   Freshness, volume, schema, distribuição/valores e lineage.
   :::
4. Duas formas de detectar anomalias?
   :::{dropdown} Resposta
   Regras/limiares (ex.: volume não cai >30% vs média) e estatística/ML (faixa normal, média ± k·desvio). Comece pelas regras.
   :::
5. O que é data downtime?
   :::{dropdown} Resposta
   O tempo em que os dados estão errados ou indisponíveis sem ninguém saber; observabilidade reduz o tempo de detecção e de resolução.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você saberia que um pipeline quebrou antes do usuário reclamar?"
  :::{dropdown} Resposta modelo
  Observabilidade: monitor de freshness (alerta se a tabela não atualizou no SLA), de volume (queda/pico vs histórico), de schema (coluna/tipo mudou) e de distribuição (nulos/média fora do padrão), com alertas automáticos e lineage para achar a causa. Reduz o data downtime.
  :::
- **P:** "Regras ou ML para anomalia?"
  :::{dropdown} Resposta modelo
  Começo por regras/limiares simples e transparentes (variação de volume, % de nulos, SLA de freshness) — fáceis de entender e ajustar. ML de anomalia entra depois, para padrões que regras não capturam, aceitando menos transparência.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (observabilidade, data downtime).
- **dbt docs** — *Source freshness*.

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — observabilidade. <!-- @reis2022 -->
- Densmore, J. *Data Pipelines Pocket Reference* (2021) — monitoramento de pipelines. <!-- @densmore2021 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — confiabilidade. <!-- @kleppmann2017 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
