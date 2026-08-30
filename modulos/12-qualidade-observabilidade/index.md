# Módulo 12 — Qualidade, Testes e Observabilidade de Dados

> Dados errados são piores que dados ausentes. Garantir confiança no que você entrega.

## Identificação
- **Eixo:** 4 — Escala, Qualidade e Governança
- **Carga horária:** 25h
- **Pré-requisitos:** M07, M09
- **Onde roda:** Bancada Docker

## Ementa
Dimensões de qualidade de dados (completude, unicidade, validade, consistência,
atualidade). Testes de dados com dbt e com Great Expectations. Data contracts. Observabilidade
de pipelines: métricas, freshness, volume, anomalias. Monitoramento e alertas. Cultura de
confiabilidade (data downtime).

## Competências e habilidades
- C10 — garantir qualidade, testes e observabilidade de dados.

## Objetivos de aprendizagem
1. **Definir** checagens de qualidade para um dataset.
2. **Implementar** testes com dbt e/ou Great Expectations.
3. **Monitorar** freshness/volume e configurar alertas.
4. **Explicar** o conceito de data contract.

## Plano de aulas (unidades)

**Unidade 1 — Dimensões de qualidade e data contracts**
1. **Teoria:** [Dimensões de qualidade e data contracts](teoria-01-dimensoes-qualidade-contracts.md)
2. **Exercícios:** [Completude (🟢)](exercicio-01.md) · [Validar contrato (🟢)](exercicio-02.md)

**Unidade 2 — Testes de dados (dbt + Great Expectations)**
1. **Teoria:** [Testes: dbt e Great Expectations](teoria-02-testes-dbt-ge.md)
2. **Lab:** [Checagens de qualidade como queries](lab-01-checagens-qualidade.ipynb)
3. **Exercícios:** [Unicidade: duplicados (🟢)](exercicio-03.md) · [Validade: fora do domínio (🟢)](exercicio-04.md)

**Unidade 3 — Observabilidade: freshness, volume, anomalias**
1. **Teoria:** [Observabilidade: freshness, volume, anomalias](teoria-03-observabilidade-freshness-anomalias.md)
2. **Exercícios:** [Freshness/SLA (🟢)](exercicio-05.md) · [Anomalia de volume (🟢)](exercicio-06.md)

**Unidade 4 — Monitoramento e alertas**
1. **Teoria:** [Monitoramento, alertas e confiabilidade](teoria-04-monitoramento-alertas.md)
2. **Exercícios:** [Deve alertar? (🟢)](exercicio-07.md) · [Fora da faixa (🟢)](exercicio-08.md)

> **Módulo completo.** Qualidade + observabilidade — a confiança que sustenta todo o resto.

## Metodologia e avaliação
**Maestria:** suíte de qualidade sobre um pipeline com alerta em falha, conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Qualidade/observabilidade viraram requisito; mostrar isso no portfólio impressiona.

## Erros comuns
- Testar só o código, nunca os dados.
- Não monitorar freshness (pipeline "verde" mas com dados velhos).
- Alertas ruidosos que todos ignoram.

## Recursos
A curar em `recursos.md` (docs do Great Expectations; testes do dbt).

---
**Revisado em:** 2026-08-20
