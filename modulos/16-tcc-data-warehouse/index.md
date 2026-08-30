# Módulo 16 — TCC: Implementação de um Data Warehouse completo

> O capstone. Você integra tudo — modelagem, dbt, ingestão, Airflow, Docker e qualidade —
> num Data Warehouse de e-commerce que responde perguntas de negócio de ponta a ponta.

## Identificação
- **Eixo:** 5 — Carreira e Integração
- **Carga horária:** 60h
- **Pré-requisitos:** Eixos 1–4 (M05 modelagem · M06 DW · M07 dbt · M08 ingestão · M09 Airflow · M10 Docker · M12 qualidade)
- **Onde roda:** Bancada Docker (Postgres/dbt/Airflow) + opcional BigQuery free-tier

## Ementa
Projeto final que recombina todo o curso: a construção de um **Data Warehouse dimensional**
sobre o dataset **Olist** (e-commerce brasileiro), com ingestão reproduzível, camadas
raw→staging→marts, transformações **dbt** com testes e docs, orquestração **Airflow**
idempotente, conteinerização com **docker-compose**, verificações de qualidade e documentação
completa (README com arquitetura, ADRs e relatório). Entrega publicada no GitHub + defesa gravada.

A especificação técnica completa está em [`tcc/especificacao-dw.md`](../../tcc/especificacao-dw.md)
e o regulamento (regras e avaliação) em [Regulamento do TCC](../../ppc/regulamento-do-tcc.md).
Um **scaffold inicial** (estrutura de repositório pronta para você preencher) está em
[`tcc/starter/`](../../tcc/starter/).

## Competências e habilidades
- C14 — projetar e implementar um Data Warehouse completo, integrando o stack do curso.

## Objetivos de aprendizagem
1. **Projetar** um modelo dimensional (star schema) com SCD Tipo 2 para um domínio real.
2. **Implementar** o pipeline ELT (ingestão → dbt → marts) com testes e docs.
3. **Orquestrar** o pipeline com Airflow de forma idempotente e agendada.
4. **Empacotar** tudo com docker-compose e **documentar** para reprodutibilidade.
5. **Defender** as decisões de arquitetura (arguição crítica).

## Plano de trabalho (etapas)

**Etapa 1 — Planejamento, escopo e setup**
- **Guia:** [Planejamento, escopo e setup do repositório](etapa-01-planejamento-setup.md)

**Etapa 2 — Modelagem dimensional (o coração do DW)**
- **Guia:** [Modelagem dimensional: grão, fato, dimensões, SCD2](etapa-02-modelagem-dimensional.md)

**Etapa 3 — Ingestão e transformação (dbt)**
- **Guia:** [Ingestão reproduzível e camadas dbt com testes](etapa-03-ingestao-dbt.md)

**Etapa 4 — Orquestração, empacotamento e entrega**
- **Guia:** [Airflow, docker-compose, documentação e defesa](etapa-04-orquestracao-entrega.md)

> **Este é o fim da trilha.** Ao concluir o TCC você terá, no GitHub, a prova de ponta a ponta
> de que constrói uma plataforma de dados — o ativo central do seu portfólio (M15).

## Metodologia e avaliação
**Maestria:** repositório reproduzível (um terceiro sobe com `docker compose up` e roda seguindo
o README), modelo dimensional com SCD2, dbt com testes verdes, DAG Airflow idempotente,
relatório (6–12 págs) e vídeo de defesa (5–10 min) — conforme a rubrica do
[Regulamento do TCC](../../ppc/regulamento-do-tcc.md).

## O que o mercado espera
Um projeto assim **é** o que se pede numa vaga de Data Engineer júnior/pleno: pipeline real,
versionado, testado e documentado. Bem apresentado (M15), costuma ser o diferencial que fecha a contratação.

## Erros comuns
- Começar a codar sem definir o **grão** da fato (retrabalho garantido).
- dbt sem testes; DAG sem idempotência (recarga duplica dados).
- README que não permite a um terceiro subir o projeto.
- Deixar a documentação/relatório para o fim e não terminar.

## Recursos
Ver [`recursos.md`](recursos.md), a [especificação](../../tcc/especificacao-dw.md) e o
[scaffold](../../tcc/starter/).

---
**Revisado em:** 2026-08-30
