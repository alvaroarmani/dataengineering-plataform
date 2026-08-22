# Projeto Integrador — Eixo 3 (Pipelines e Orquestração)

> **Pipeline orquestrado com Airflow**, conteinerizado, ingerindo de uma API real.

## Objetivo
Automatizar um fluxo ELT: ingestão incremental de uma **API** → armazenamento → transformação,
orquestrado por uma **DAG Airflow idempotente**, tudo rodando via `docker-compose`.

## Requisitos
1. Ingestão **incremental** de uma API (ex.: câmbio do Banco Central).
2. **DAG Airflow** agendada, idempotente (reprocessar um dia não duplica dados).
3. Tratamento de falhas (retries) e um teste de qualidade pós-carga.
4. **`docker-compose`** que sobe Airflow + banco.
5. README com o diagrama do fluxo.

## Entregáveis
- Repositório GitHub com a DAG, o compose e documentação.

## Rubrica
Ver [rubrica genérica](../../ppc/metodologia-e-avaliacao.md), com peso extra em **robustez/idempotência**.

---
**Revisado em:** 2026-08-20
