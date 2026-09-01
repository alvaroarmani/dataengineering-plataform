# Projeto Integrador — Eixo 3 (Pipelines e Orquestração)

> **Pipeline ELT orquestrado.** Ingira de uma **API real**, integre de forma incremental e
> idempotente, com um portão de qualidade — primeiro em funções puras (auto-corrigível), depois
> numa **DAG Airflow** conteinerizada. Um clássico de portfólio de Data Engineer.

## 🎯 Objetivo
Automatizar um fluxo de dados **confiável**:
1. **Ingestão** de uma API (cotação de câmbio) → normalização;
2. **Carga incremental e idempotente** (reprocessar um dia **não** duplica);
3. **Portão de qualidade** (barra dados nulos/negativos/duplicados);
4. **Orquestração** com uma **DAG Airflow** agendada, com retries — na bancada.

## 📦 Fonte
Uma **API pública** (ex.: cotação do dólar PTAX do Banco Central, ou IBGE). Os testes usam uma
**amostra** da resposta (`starter/data/amostra_api.json`) — na trilha real você chama a API de verdade.

## 🧭 Etapas e requisitos

**Trilha A — núcleo auto-corrigível (pandas).** Em `starter/pipeline.py`, implemente:
- `parse_cotacoes(payload)` → `[data, valor]` ordenado por data.
- `upsert_idempotente(destino, novos)` → integra por `data` (novos prevalecem), 1 linha por data; idempotente.
- `checar_qualidade(df)` → lista ordenada de problemas (`data_duplicada`, `valor_negativo`, `valor_nulo`).

Faça `pytest -q` passar (3 testes).

**Trilha B — orquestração real com Airflow (bancada Docker) 🐳.** Complete a DAG em
`starter/dags/dag_cambio.py` (reusando as funções puras) e valide com
`airflow dags test dag_cambio 2026-08-10` (como no [M09](../../modulos/09-orquestracao-airflow/index.md)).
A DAG deve ser agendada, **idempotente** e falhar quando a qualidade não passa.

## ✅ Entregáveis
- Repositório **no GitHub** com a **trilha A verde** (`pytest`) e, idealmente, a **DAG rodando** (trilha B).
- **README** com um **diagrama do fluxo** (mermaid), como rodar e os achados.
- Parágrafo **Situação → Ação → Resultado** para o currículo (M15).

## 📊 Rubrica (0–100)
| Critério | Peso |
|---|---|
| Ingestão + parsing corretos | 20 |
| **Idempotência** da carga (reprocessar não duplica) | 30 |
| Portão de qualidade (barra dados ruins) | 20 |
| Orquestração Airflow (DAG agendada, retries) | 15 |
| Documentação (README + diagrama) | 15 |

Conceito mínimo para "concluído": **60**, sem nenhum critério zerado.

## 💡 Dicas (hint ladder)
:::{dropdown} Dica 1 — parsing
Liste dicts `{"data": v["dataHoraCotacao"][:10], "valor": v["cotacaoCompra"]}` e vire um DataFrame ordenado por data.
:::
:::{dropdown} Dica 2 — upsert idempotente
`pd.concat([destino, novos])` e `drop_duplicates(subset="data", keep="last")` — os novos vêm por último, então prevalecem.
:::
:::{dropdown} Dica 3 — DAG idempotente
Cada execução é "dona" do seu dia: apague/sobrescreva a partição daquele dia antes de inserir (padrão do M09, ex-05).
:::

---
**Revisado em:** 2026-08-31
