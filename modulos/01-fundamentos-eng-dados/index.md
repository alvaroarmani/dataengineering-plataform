# Módulo 01 — Fundamentos de Engenharia de Dados e Arquitetura

> Ao final, você entenderá **o que faz** um engenheiro de dados, o **ciclo de vida do dado** e as principais **arquiteturas** — e já terá tocado em dados reais.

## Perguntas essenciais
Ao final deste módulo, você saberá responder:
1. O que faz (e o que **não** faz) um engenheiro de dados, e onde ele se encaixa no time?
2. Por que separamos sistemas **OLTP** de **OLAP** — e o que isso tem a ver com armazenamento colunar?
3. Quando usar **Data Warehouse**, **Data Lake** ou **Lakehouse**; batch ou streaming?

## Identificação
- **Eixo:** 1 — Fundamentos
- **Carga horária:** 30h
- **Pré-requisitos:** —
- **Onde roda:** Browser (JupyterLite) para o lab; leitura de teoria no navegador

## Ementa
Panorama da Engenharia de Dados: o papel do engenheiro e sua relação com analistas,
cientistas e o negócio. Ciclo de vida do dado (geração, ingestão, armazenamento,
transformação, disponibilização). OLTP vs OLAP. Batch vs streaming. Formatos de dados e
armazenamento colunar. Arquiteturas: Data Warehouse, Data Lake, Lakehouse, Modern Data
Stack, Lambda/Kappa e noções de Data Mesh.

## Competências e habilidades
- Compreender o escopo da Engenharia de Dados e onde ela se encaixa (C-transversal).
- Distinguir cargas OLTP/OLAP e abordagens batch/streaming.
- Ler dados reais com uma ferramenta analítica (pandas/DuckDB).

## Objetivos de aprendizagem
Ao final, você será capaz de:
1. **Explicar** o ciclo de vida do dado e o papel do engenheiro.
2. **Diferenciar** OLTP de OLAP e batch de streaming, com exemplos.
3. **Descrever** DW, Data Lake e Lakehouse e quando cada um faz sentido.
4. **Carregar e inspecionar** um dataset real em um notebook.

## Pré-requisitos e "testar para pular"
Não há pré-requisitos. Se você já atua com dados e sabe explicar OLTP vs OLAP, star schema
e batch vs streaming, faça o [exercício](exercicio-01.md) direto — passando, pode avançar ao M02.

## Plano de aulas (unidades)
1. **Teoria:** [O que é Engenharia de Dados](teoria-01-o-que-e-engenharia-de-dados.md)
2. **Lab:** [Primeiro contato com dados](lab-01-primeiro-contato-dados.ipynb)
3. **Exercício:** [Exercício 01](exercicio-01.md)
4. **Revisão:** [Flashcards](flashcards.md)

## Metodologia e avaliação
Ciclo problema → teoria → lab → exercício → revisão. **Critério de maestria:**
`pytest` verde no exercício + quiz de recall ≥ 80% + saber explicar as arquiteturas.

## O que o mercado espera
Que você entenda o **panorama** e o vocabulário: saber onde entram DW, lake, batch,
streaming, e qual problema cada arquitetura resolve. Isso aparece em entrevistas como
perguntas conceituais ("quando usar data lake vs data warehouse?").

## Erros comuns de iniciantes
- Achar que "engenharia de dados = pandas". A área é sobre **sistemas e confiabilidade**.
- Confundir **OLTP** (transacional) com **OLAP** (analítico).
- Tratar **data lake** e **data warehouse** como sinônimos.

## Projeto do módulo
Este módulo alimenta o [Projeto Integrador do Eixo 1](../../projetos/eixo-1-fundamentos/index.md).

## Recursos e bibliografia
Ver [recursos.md](recursos.md).

---
**Revisado em:** 2026-08-20
