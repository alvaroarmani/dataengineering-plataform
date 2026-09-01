# Projeto Integrador — Eixo 2 (Data Warehousing e Modelagem)

> **Star schema + dbt.** Modele dimensionalmente um e-commerce e implemente as transformações —
> primeiro em pandas (auto-corrigível), depois em **dbt** sobre a bancada. O núcleo do futuro TCC,
> e uma peça forte de portfólio.

## 🎯 Objetivo
Transformar dados brutos num **modelo dimensional** (star schema) pronto para análise:
1. **Dimensão** com **chave substituta** (surrogate key);
2. **Fato** no **grão** de pedido, com FK substituta e medida (`receita`);
3. **SCD Tipo 2** (histórico da categoria de um produto);
4. **Testes** de qualidade (grão único, chaves não nulas) — e, na trilha real, `dbt build`.

## 📦 Dataset
Seeds pequenos em `starter/data/` (produtos, pedidos e um **histórico** para o SCD2). Depois,
desafie-se a trocar pelo **Olist** real (ver [datasets](../../datasets/README.md)) — é o mesmo
domínio do TCC.

## 🧭 Etapas e requisitos

**Trilha A — núcleo auto-corrigível (pandas).** Em `starter/modelagem.py`, implemente:
- `construir_dim_produto(raw_produtos)` → `[produto_sk, produto_id, nome, categoria]` (sk sequencial).
- `construir_fct_vendas(raw_pedidos, dim_produto)` → fato no grão de pedido, com `produto_sk` (FK) e `receita = valor × quantidade`.
- `aplicar_scd2(historico)` → dimensão SCD2 com `valido_de`, `valido_ate` (`'9999-12-31'` na atual), `is_current`.

Faça `pytest -q` passar (4 testes).

**Trilha B — a versão real em dbt (bancada Docker) 🐳.** Reproduza o modelo em **dbt sobre Postgres**
(como no [M07](../../modulos/07-transformacao-dbt/index.md)): complete `dbt/models/` (staging → marts)
e o `dbt/snapshots/` (SCD2), com testes `unique`/`not_null`/`relationships`, e rode `dbt build`.

## ✅ Entregáveis
- Repositório **no GitHub** com a **trilha A verde** (`pytest`) e, idealmente, a **trilha B** (`dbt build` verde).
- **README** com um **diagrama do star schema** (mermaid), como rodar e os achados.
- Parágrafo **Situação → Ação → Resultado** para o currículo (M15).

## 📊 Rubrica (0–100)
| Critério | Peso |
|---|---|
| Modelagem correta (grão, fato × dimensão, surrogate key) | 30 |
| SCD Tipo 2 correto (histórico versionado) | 20 |
| Testes de qualidade (grão único, chaves não nulas) | 20 |
| Trilha real em dbt (build + testes verdes) | 15 |
| Documentação (README + diagrama) | 15 |

Conceito mínimo para "concluído": **60**, sem nenhum critério zerado.

## 💡 Dicas (hint ladder)
:::{dropdown} Dica 1 — surrogate key
Ordene por `produto_id`, `reset_index(drop=True)` e `insert(0, "produto_sk", range(1, len(df)+1))`.
:::
:::{dropdown} Dica 2 — fato com FK substituta
`merge` dos pedidos com `dim_produto[["produto_sk","produto_id"]]` por `produto_id`; então `receita = valor*quantidade`.
:::
:::{dropdown} Dica 3 — SCD2
Ordene por `produto_id, data`; para cada produto, `valido_ate` de uma versão é a `data` da próxima (ou `'9999-12-31'`); `is_current` só na última.
:::

---
**Revisado em:** 2026-08-31
