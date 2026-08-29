# Módulo 07 — Transformação de Dados com dbt

> ELT moderno: transformar dados com SQL versionado, testado e documentado.

## Identificação
- **Eixo:** 2 — Data Warehousing e Modelagem
- **Carga horária:** 30h
- **Pré-requisitos:** M06
- **Onde roda:** 🐳 Bancada Docker (dbt + Postgres real) — com espelho no navegador (DuckDB) por unidade

## Ementa
Paradigma ELT e o papel do dbt. Estrutura de um projeto dbt: `sources`, `models`
(staging/marts), materializações (view, table, incremental). Testes de dados
(`unique`, `not_null`, `relationships`, `accepted_values`). Documentação e lineage
(`dbt docs`). Macros e Jinja. Boas práticas de organização (camadas).

## Competências e habilidades
- C6 — transformar dados com dbt (ELT, testes, lineage).

## Objetivos de aprendizagem
1. **Estruturar** um projeto dbt em camadas (staging → marts).
2. **Escrever** modelos e escolher materializações adequadas.
3. **Adicionar** testes de dados e gerar documentação/lineage.
4. **Usar** macros/Jinja para reduzir repetição.

## Plano de aulas (unidades)

**Unidade 1 — Fundamentos: ELT, sources e staging**
1. **Teoria:** [dbt: transformação como código](teoria-01-dbt-fundamentos.md)
2. **Lab (🐳 dbt real):** [dbt na bancada: seu primeiro build](lab-01-dbt-na-bancada.md)
3. **Exercícios:** [Seu primeiro model dbt (🐳 real)](exercicio-01.md) · [Staging + mart (🟢 navegador)](exercicio-02.md)

_Próximas unidades (em construção): marts dimensionais · testes de dados (unique/not_null/relationships) · snapshots (SCD2), docs, lineage e macros._

## Metodologia e avaliação
**Maestria:** projeto dbt sobre o star schema com testes passando + `dbt docs`, conforme rubrica.

## O que o mercado espera
dbt é padrão de fato no *analytics engineering*; aparece em muitas vagas. Saber testar e documentar conta muito.

## Erros comuns
- Não separar camadas (staging vs marts).
- Materializar tudo como `table` sem pensar em custo.
- Esquecer testes de integridade (`relationships`).

## Recursos
A curar em `recursos.md` (docs do dbt; dbt Fundamentals).

---
**Revisado em:** 2026-08-20
