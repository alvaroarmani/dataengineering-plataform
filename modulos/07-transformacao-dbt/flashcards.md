# Flashcards — Módulo 07

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** O que é o dbt e qual parte do ELT ele cobre? / **R:** A ferramenta de transformação (o "T" do ELT): você escreve SELECTs e ele materializa tabelas/views no warehouse, com dependências, testes e docs.
- **P:** O que é um "model" no dbt? / **R:** Um arquivo .sql com um SELECT; o dbt gera o DDL e materializa o resultado (view por padrão). Você não escreve CREATE TABLE.
- **P:** `source()` vs `ref()`? / **R:** source() referencia tabelas cruas (sources.yml); ref() referencia outro model. Juntos formam o DAG de dependências e o lineage.
- **P:** O que faz `dbt build`? / **R:** Roda na ordem do DAG: seed → run (materializa models) → test → snapshot.
- **P:** Para que serve a camada de staging (stg_*)? / **R:** Limpeza leve 1:1 com a fonte (renomear, converter tipos, padronizar), sem regra de negócio — base para os marts.
- **P:** Materializações do dbt? / **R:** view (padrão, leve), table (materializa fisicamente), incremental (só o que mudou), ephemeral (vira CTE, sem objeto no DW).
- **P:** Por que ELT em vez de ETL? / **R:** DWs cloud baratos/elásticos tornam prático carregar cru e transformar dentro do warehouse, versionando as transformações como código (testes, revisão, CI).
- **P:** Quais as camadas de um projeto dbt? / **R:** staging (stg_*, limpeza 1:1), intermediate (int_*, opcional) e marts (fct_*/dim_*, consumo dimensional).
- **P:** Por que um mart usa ref('stg_...') e não a tabela crua? / **R:** Para respeitar camadas e construir o DAG/lineage — o dbt roda o staging antes e sabe as dependências.
- **P:** Materialização de staging vs marts? / **R:** Staging como view (leve, sempre fresco); marts como table (lidos muito por dashboards — vale materializar).
- **P:** Onde vai a regra de negócio: staging ou mart? / **R:** No mart (ou intermediate). Staging é limpeza 1:1, sem regra de negócio.
- **P:** Os 4 testes genéricos do dbt? / **R:** not_null, unique, accepted_values (valor numa lista) e relationships (integridade referencial — FK existe na outra tabela).
- **P:** Como um teste dbt passa ou falha? / **R:** É uma query que busca violações; 0 linhas = passa, qualquer linha = falha.
- **P:** O que é um teste singular? / **R:** Um SELECT em tests/*.sql que retorna o que não deveria existir (ex.: receita < 0).
- **P:** O que é um snapshot do dbt? / **R:** SCD2 automático: versiona mudanças de uma fonte mutável com dbt_valid_from/to, por strategy timestamp ou check.
- **P:** O que o `dbt docs` oferece de mais valioso? / **R:** O grafo de lineage (DAG de ref/source) para impact analysis, além das descrições e testes.
- **P:** O que é um macro no dbt? / **R:** Um trecho de SQL reutilizável em Jinja ({% macro %}); ref/source/config são macros; dbt_utils traz prontos (generate_surrogate_key).

---
**Revisado em:** 2026-08-24
