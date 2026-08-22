# Projeto Integrador — Eixo 1 (Fundamentos)

> **Mini-pipeline batch local** que integra Python, SQL e Git. Primeiro item do seu portfólio.

## Objetivo
Construir um pipeline simples e **reproduzível** que baixa um dataset real, limpa/transforma
com Python, carrega em Postgres e responde perguntas com SQL — tudo versionado no GitHub.

## Dataset
NYC Taxi (um mês) ou Olist (pedidos) — ver [datasets](../../datasets/README.md).

## Requisitos
1. Script Python que lê o dataset e faz limpeza (tipos, nulos, colunas).
2. Carga em **Postgres** (bancada Docker).
3. **5 consultas SQL** que respondem perguntas de negócio (inclua ao menos 1 window function).
4. **Testes** (`pytest`) para as funções de transformação.
5. **README** com arquitetura, como rodar e resultados.

## Entregáveis
- Repositório GitHub + "Situação → Ação → Resultado" para o currículo.

## Rubrica
Ver [rubrica genérica](../../ppc/metodologia-e-avaliacao.md).

## Dicas
:::{dropdown} Dica 1 — estrutura
Separe `ingest.py`, `transform.py`, `load.py` e `sql/`. Facilita testar e explicar.
:::
:::{dropdown} Dica 2 — reprodutibilidade
Documente no README o comando único que sobe o Postgres e roda o pipeline.
:::

---
**Revisado em:** 2026-08-20
