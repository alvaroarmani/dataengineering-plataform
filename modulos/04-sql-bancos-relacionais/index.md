# Módulo 04 — SQL e Bancos de Dados Relacionais

> A competência mais usada no dia a dia: SQL do básico ao avançado, com PostgreSQL.

## Perguntas essenciais
Ao final deste módulo, você saberá responder:
1. Como estruturar e consultar dados num banco relacional (PK/FK, SELECT, JOIN)?
2. Como resumir dados com `GROUP BY`, subqueries, CTEs e **window functions**?
3. Por que uma query é lenta — e como índices e o plano de execução ajudam?

## Identificação
- **Eixo:** 1 — Fundamentos
- **Carga horária:** 45h
- **Pré-requisitos:** M02
- **Onde roda:** Bancada Docker (Postgres) + Browser (DuckDB)

## Ementa
Modelo relacional e álgebra básica. SQL: SELECT, filtros, JOINs, agregações, GROUP BY,
subqueries e CTEs. Funções de janela (window functions). Índices e noções de performance
(plano de execução). Transações e ACID. Introdução a NoSQL (quando e por quê).

## Competências e habilidades
- C2 — escrever SQL avançado e modelar bancos relacionais.

## Objetivos de aprendizagem
1. **Escrever** consultas com JOINs, agregações, subqueries e CTEs.
2. **Aplicar** window functions em problemas analíticos.
3. **Explicar** e melhorar performance com índices (ler o `EXPLAIN`).
4. **Compreender** transações/ACID e o papel do NoSQL.

## Plano de aulas (unidades)

**Unidade 1 — Modelo relacional e SELECT**
1. **Teoria:** [Modelo relacional e o SELECT](teoria-01-modelo-relacional-select.md)
2. **Lab:** [SQL no navegador (DuckDB)](lab-01-sql-no-navegador.ipynb)
3. **Exercício:** [Suas primeiras queries](exercicio-01.md)

_Próximas unidades (em construção): JOINs e agregações · subqueries e CTEs · window functions · índices e performance · transações/ACID e NoSQL._

## Metodologia e avaliação
**Maestria:** bateria de desafios SQL (autocorrigidos) + quiz ≥ 80%. SQL entra também nos
desafios semanais.

## O que o mercado espera
SQL fluente é *o* filtro de entrevistas Jr/Pleno — window functions e CTEs caem sempre.

## Erros comuns
- Confundir `WHERE` e `HAVING`.
- Fazer no Python o que o banco faria melhor.
- Ignorar índices e ler planos de execução.

## Recursos
A curar em `recursos.md` (Tanimura *SQL for Data Analysis*; docs do PostgreSQL; pgexercises).

---
**Revisado em:** 2026-08-20
