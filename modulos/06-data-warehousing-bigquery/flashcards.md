# Flashcards — Módulo 06

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** OLTP vs OLAP? / **R:** OLTP = transacional (muitas escritas pequenas, roda a operação); OLAP = analítico (leituras que varrem/agregam grandes volumes). Cargas opostas — por isso o DW é separado.
- **P:** O que é um Data Warehouse (Inmon)? / **R:** Coleção de dados orientada a assunto, integrada, não-volátil e variável no tempo (histórica), para análise e decisão.
- **P:** Quais as camadas de um DW? / **R:** Staging/raw (cru), core/integrado (limpo, fonte da verdade), marts/consumo (dimensional para BI). No lakehouse: bronze/prata/ouro.
- **P:** Inmon vs Kimball? / **R:** Inmon = top-down, EDW normalizado primeiro; Kimball = bottom-up, marts dimensionais por processo integrados por dimensões conformadas. Híbridos são comuns.
- **P:** O que é uma dimensão conformada? / **R:** Dimensão compartilhada entre vários fatos/marts (mesma dim_cliente em vendas e devoluções); garante que os números batam e evita ilhas de dados.
- **P:** DW vs data lake? / **R:** Lake guarda dados crus (arquivos, barato/flexível); DW guarda dados modelados e limpos para consulta analítica. Lakehouse une os dois com camadas.
- **P:** Por que não analisar no banco de produção? / **R:** OLTP e OLAP têm cargas antagônicas; consultas analíticas competem com as transações e degradam a operação.

---
**Revisado em:** 2026-08-23
