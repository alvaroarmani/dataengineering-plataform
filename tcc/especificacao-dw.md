# TCC — Especificação do Data Warehouse

Especificação técnica do trabalho final. O regulamento (regras, avaliação) está em
[Regulamento do TCC](../ppc/regulamento-do-tcc.md).

## Visão

Construir um **Data Warehouse analítico** de ponta a ponta para um domínio de e-commerce,
usando o **dataset Olist** (opcionalmente enriquecido com uma API), modelado
dimensionalmente, transformado com dbt, orquestrado com Airflow e conteinerizado — pronto
para responder perguntas de negócio.

## Perguntas de negócio (exemplos que o DW deve responder)

- Receita e nº de pedidos por mês, estado e categoria de produto.
- Ticket médio e tempo médio de entrega por região.
- Taxa de reviews negativos por vendedor/categoria.
- Coorte de clientes recorrentes vs. únicos.

## Arquitetura-alvo (local-first + BigQuery)

```{mermaid}
flowchart LR
    S[Fontes: CSV Olist + API] --> I[Ingestão batch<br/>Python/Airflow]
    I --> R[(raw / bronze)]
    R --> ST[staging / silver<br/>dbt]
    ST --> M[marts / gold<br/>star schema<br/>dbt]
    M --> BI[Consumo analítico<br/>SQL / BI]
    subgraph Armazenamento
      R --> DW[(Postgres local ou BigQuery)]
      ST --> DW
      M --> DW
    end
```

Você pode entregar em **Postgres local** (mais simples) ou **BigQuery** (mais próximo do
mercado). Recomendado: desenvolver local e publicar uma versão em BigQuery.

## Modelagem (mínimo)

- **Fato:** `fct_pedidos` (grão: item de pedido) com métricas (valor, frete, etc.).
- **Dimensões:** `dim_cliente`, `dim_produto`, `dim_vendedor`, `dim_data`, `dim_geografia`.
- **SCD:** trate ao menos uma dimensão como **SCD Tipo 2** (ex.: mudança de categoria/localização).

## Requisitos técnicos

1. Ingestão reproduzível (script + DAG Airflow idempotente).
2. Camadas raw → staging → marts.
3. Transformações **dbt** com **testes** (`unique`, `not_null`, `relationships`) e docs/lineage.
4. Orquestração **Airflow** agendada, com tratamento de falha e reprocessamento seguro.
5. **`docker-compose`** que sobe o stack.
6. Verificações de **qualidade** e um mínimo de **observabilidade** (log/execução).
7. **Documentação:** README com arquitetura (diagrama), ADRs de decisão, e um relatório (6–12 págs).
8. Publicação no **GitHub** + apresentação gravada (5–10 min).

## Entregáveis

- Repositório GitHub reproduzível (um terceiro sobe e roda seguindo o README).
- Relatório + vídeo de defesa.

## Como começar (quando chegar a hora)

O TCC recombina tudo: modelagem (M05), DW/BigQuery (M06), dbt (M07), ingestão (M08),
Airflow (M09), Docker (M10) e qualidade (M12). Use a IA como **banca**: peça arguição
crítica das suas decisões de arquitetura.

---
**Revisado em:** 2026-08-20
