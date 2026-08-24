# Módulo 05 — Modelagem de Dados e Dimensional Modeling (Kimball)

> O coração do Data Warehouse: modelar fatos e dimensões para análise.

## Perguntas essenciais
Ao final deste módulo, você saberá responder:
1. Qual a diferença entre fato e dimensão — e como declarar o **grão** correto?
2. Quando usar star schema vs snowflake, e por que desnormalizar para análise?
3. Como lidar com atributos que mudam no tempo (SCD) e por que usar surrogate keys?

## Identificação
- **Eixo:** 2 — Data Warehousing e Modelagem
- **Carga horária:** 40h
- **Pré-requisitos:** M04
- **Onde roda:** Bancada Docker (Postgres)

## Ementa
Normalização (1FN–3FN) e por que desnormalizamos para análise. Modelagem dimensional
segundo Kimball: tabelas fato e dimensão, grão, star schema vs snowflake. Chaves substitutas
(surrogate keys). Slowly Changing Dimensions (SCD tipos 1, 2 e 3). Modelagem a partir de
processos de negócio.

## Competências e habilidades
- C4 — modelar dados dimensionalmente (Kimball).

## Objetivos de aprendizagem
1. **Definir** o grão de uma tabela fato e suas dimensões.
2. **Projetar** um star schema a partir de um processo de negócio.
3. **Implementar** surrogate keys e uma dimensão **SCD Tipo 2**.
4. **Justificar** escolhas de modelagem (star vs snowflake).

## Plano de aulas (unidades)

**Unidade 1 — Fatos, dimensões e grão**
1. **Teoria:** [Fatos, dimensões e grão](teoria-01-fatos-dimensoes-grao.md)
2. **Lab:** [Um star schema na prática](lab-01-star-schema.ipynb)
3. **Exercício:** [Consultando um star schema](exercicio-01.md)

**Unidade 2 — Surrogate keys (chaves substitutas)**
1. **Teoria:** [Surrogate keys](teoria-02-surrogate-keys.md)
2. **Lab:** [Surrogate keys na prática](lab-02-surrogate-keys.ipynb)
3. **Exercício:** [Gerar e usar surrogate keys](exercicio-02.md)

**Unidade 3 — Slowly Changing Dimensions (SCD)**
1. **Teoria:** [SCDs: versionando o histórico](teoria-03-scd.md)
2. **Lab:** [SCD Tipo 2 na prática](lab-03-scd.ipynb)
3. **Exercício:** [Consultando uma dimensão SCD2](exercicio-03.md)

**Unidade 4 — Modelando a partir de um processo de negócio (Olist)**
1. **Teoria:** [Modelando a partir de um processo de negócio](teoria-04-modelando-processo-negocio.md)
2. **Lab:** [Modelando o Olist: do staging ao star](lab-04-modelar-olist.ipynb)
3. **Exercício:** [Analisando o star schema do Olist](exercicio-04.md)

> **Módulo completo.** A modelagem dimensional aprendida aqui será consolidada no projeto integrador do Eixo 2 e no TCC (Data Warehouse).

## Metodologia e avaliação
**Maestria:** projetar e implementar um star schema (Olist) com uma SCD2, conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Saber modelar e **explicar** o porquê (grão, SCD) diferencia muito candidatos Jr.

## Erros comuns
- Não definir o **grão** antes de modelar.
- Usar chaves naturais onde surrogate keys seriam melhores.
- Ignorar mudanças históricas (SCD) nas dimensões.

## Recursos
A curar em `recursos.md` (Kimball & Ross *The Data Warehouse Toolkit*).

---
**Revisado em:** 2026-08-20
