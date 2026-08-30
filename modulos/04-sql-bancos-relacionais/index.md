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
1. **Teoria:** [Modelo relacional e o SELECT](teoria-01-modelo-relacional-select.md) · **Lab:** [SQL no navegador](lab-01-sql-no-navegador.ipynb) · **Exercícios:** [Primeiras queries](exercicio-01.md) · [SELECT: filtro e agregação](exercicio-06.md)

**Unidade 2 — JOINs e agregações**
2. **Teoria:** [JOINs e agregações](teoria-02-joins-e-agregacoes.md) · **Lab:** [JOINs](lab-02-joins.ipynb) · **Exercícios:** [JOINs](exercicio-02.md) · [JOIN e agregação](exercicio-07.md)

**Unidade 3 — Subqueries e CTEs**
3. **Teoria:** [Subqueries e CTEs](teoria-03-subqueries-e-ctes.md) · **Lab:** [Subqueries e CTEs](lab-03-subqueries-ctes.ipynb) · **Exercícios:** [Subqueries e CTEs](exercicio-03.md) · [Subquery e CTE (2)](exercicio-08.md)

**Unidade 4 — Window functions**
4. **Teoria:** [Window functions](teoria-04-window-functions.md) · **Lab:** [Window functions](lab-04-window-functions.ipynb) · **Exercícios:** [Window functions](exercicio-04.md) · [Window: row_number e acumulado](exercicio-09.md)

**Unidade 5 — Índices e performance**
5. **Teoria:** [Índices e performance](teoria-05-indices-e-performance.md) · **Lab:** [EXPLAIN e índices](lab-05-explain-e-indices.ipynb) · **Exercícios:** [HAVING e "segundo maior"](exercicio-05.md) · [Filtro seletivo](exercicio-10.md)

**Unidade 6 — Transações, ACID e NoSQL**
6. **Teoria:** [Transações, ACID e NoSQL](teoria-06-transacoes-acid-nosql.md) · **Lab:** [Transações](lab-06-transacoes.ipynb) · **Exercícios:** [Integridade: duplicatas](exercicio-11.md) · [Consistência](exercicio-12.md)

**Revisão:** [Flashcards](flashcards.md)

✅ **Módulo completo** — 6 unidades. Fecha o **Eixo 1** (Fundamentos); a seguir, o projeto integrador do eixo.

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
