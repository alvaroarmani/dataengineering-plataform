# Regulamento do TCC

## Objeto

O Trabalho de Conclusão de Curso consiste na **implementação completa de um Data
Warehouse** — da ingestão de dados de fontes reais à disponibilização de dados modelados,
testados e documentados para consumo analítico, com pipeline orquestrado e reprodutível.

A especificação técnica detalhada está em [`tcc/especificacao-dw.md`](../tcc/especificacao-dw.md).

## Pré-requisitos

Concluir por maestria os Eixos 1 a 4 (ou os módulos correspondentes via "testar para pular").

## Requisitos mínimos de entrega

1. **Ingestão** de ao menos uma fonte real (arquivo/API), em **batch**, reproduzível.
2. **Camadas** bem definidas (ex.: *raw/staging/marts* ou *bronze/silver/gold*).
3. **Modelagem dimensional** (star schema) com ao menos 1 tabela-fato e 2+ dimensões, incluindo tratamento de **SCD**.
4. **Transformações com dbt** com **testes** (unique, not_null, relationships) e **documentação/lineage**.
5. **Orquestração com Airflow** (DAG idempotente, agendada, com tratamento de falhas).
6. **Containerização** do ambiente (`docker-compose` que sobe o stack).
7. **Qualidade e observabilidade** (testes de dados + verificação de execução).
8. **Documentação**: README com arquitetura (diagrama), decisões (ADRs), instruções de reprodução e um **relatório** de 6–12 páginas.
9. **Publicação** no GitHub (build-in-public).

## Avaliação

Aplica-se a **rubrica de projeto** (ver [Metodologia e Avaliação](metodologia-e-avaliacao.md)),
com ênfase adicional em **integração** (o quanto o trabalho articula os conhecimentos dos
eixos) e **reprodutibilidade** (um terceiro consegue subir e rodar seguindo o README).

Conceito mínimo para aprovação: **60/100**, com nenhum critério zerado.

## Autoavaliação e defesa

Como o curso é autodirigido, a "defesa" é uma **apresentação gravada** (5–10 min)
explicando arquitetura, decisões e trade-offs — material valiosíssimo para o portfólio e
para entrevistas. Recomenda-se usar a **IA como banca**: peça uma arguição crítica das suas
escolhas.

---
**Revisado em:** 2026-08-20
