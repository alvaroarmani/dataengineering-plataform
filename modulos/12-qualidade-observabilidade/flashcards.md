# Flashcards — Módulo 12

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Dimensões de qualidade de dados? / **R:** Completude, unicidade, validade, consistência, freshness (atualidade) e acurácia.
- **P:** O que é um data contract? / **R:** Acordo explícito produtor↔consumidor sobre schema, semântica, garantias de qualidade e freshness — expectativas testáveis.
- **P:** O que é "shift-left" em qualidade? / **R:** Detectar problemas perto da origem (na fronteira), onde são baratos, em vez de no consumo.
- **P:** dbt tests vs Great Expectations? / **R:** dbt para dados já no DW (versionado com models); GE para validar na fronteira/ingestão e dados fora do dbt. Muitos usam os dois.
- **P:** O que todo teste de dados faz por baixo? / **R:** Uma query que busca as violações; 0 = passa.
- **P:** Pilares da observabilidade de dados? / **R:** Freshness, volume, schema, distribuição/valores e lineage.
- **P:** Como se mede freshness? / **R:** Última atualização vs agora contra um SLA (ex.: chegou nas últimas 24h?).
- **P:** O que é data downtime? / **R:** Tempo em que os dados estão errados/ausentes sem ninguém saber; observabilidade reduz detecção e resolução.
- **P:** Como evitar alert fatigue? / **R:** Alertar só no acionável, por severidade, agrupando/deduplicando e calibrando limiares.
- **P:** SLI vs SLO? / **R:** SLI é o indicador medido; SLO é a meta (ex.: 99% das cargas frescas/mês).

---
**Revisado em:** 2026-08-29
