# Flashcards — Módulo 07

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** O que é o dbt e qual parte do ELT ele cobre? / **R:** A ferramenta de transformação (o "T" do ELT): você escreve SELECTs e ele materializa tabelas/views no warehouse, com dependências, testes e docs.
- **P:** O que é um "model" no dbt? / **R:** Um arquivo .sql com um SELECT; o dbt gera o DDL e materializa o resultado (view por padrão). Você não escreve CREATE TABLE.
- **P:** `source()` vs `ref()`? / **R:** source() referencia tabelas cruas (sources.yml); ref() referencia outro model. Juntos formam o DAG de dependências e o lineage.
- **P:** O que faz `dbt build`? / **R:** Roda na ordem do DAG: seed → run (materializa models) → test → snapshot.
- **P:** Para que serve a camada de staging (stg_*)? / **R:** Limpeza leve 1:1 com a fonte (renomear, converter tipos, padronizar), sem regra de negócio — base para os marts.
- **P:** Materializações do dbt? / **R:** view (padrão, leve), table (materializa fisicamente), incremental (só o que mudou), ephemeral (vira CTE, sem objeto no DW).
- **P:** Por que ELT em vez de ETL? / **R:** DWs cloud baratos/elásticos tornam prático carregar cru e transformar dentro do warehouse, versionando as transformações como código (testes, revisão, CI).

---
**Revisado em:** 2026-08-24
