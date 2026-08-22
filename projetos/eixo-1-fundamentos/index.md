# Projeto Integrador — Eixo 1 (Fundamentos)

> **Seu primeiro projeto de portfólio.** Um mini-pipeline batch que junta tudo do Eixo 1:
> **Git** (M2), **Python/pandas** (M3) e **SQL** (M4). Ao final, você tem um repositório no
> GitHub que dá para mostrar numa entrevista.

## 🎯 Objetivo

Construir um pipeline **reproduzível** que:
1. **Ingere** um CSV de pedidos (dados sujos, como no mundo real);
2. **Limpa e transforma** com Python/pandas (funções puras + testes);
3. **Carrega** numa base (DuckDB local — zero setup);
4. **Analisa** com SQL, respondendo perguntas de negócio.

Tudo versionado no Git, com README e testes passando.

## 📦 Dataset

Um arquivo `pedidos.csv` (~20 linhas) **de propósito sujo**: alguns valores faltando, um
`valor` como texto, estados em caixa inconsistente (`sp`/`SP`). Está em
`starter/data/pedidos.csv`. (Depois, desafie-se a trocar pelo
dataset **Olist** real — ver [datasets](../../datasets/README.md).)

## 🧭 Etapas e requisitos

**1. Ingestão** — leia o CSV com pandas (`starter/pipeline/ingest.py`).

**2. Transformação** (`starter/pipeline/transform.py`) — funções **puras e testadas**:
- `padronizar_estado(df)`: coloca `estado` em maiúsculas.
- `limpar(df)`: remove linhas com `valor` inválido/ausente (quarentena).
- `adicionar_receita(df)`: cria `receita = valor * quantidade`.
- Faça `pytest` passar (testes em `starter/tests/`).

**3. Carga** (`starter/pipeline/load.py`) — grave o DataFrame limpo numa tabela DuckDB
(`pedidos`), reproduzível (rodar de novo não duplica).

**4. Análise** (`starter/consultas.sql`) — escreva **5 queries** que respondam:
- receita total por estado; top 3 categorias por receita; ticket médio por estado;
- nº de pedidos por cliente; e **uma pergunta sua** (bônus: com window function ou CTE).

## ✅ Entregáveis
- Repositório **no GitHub** com o pipeline rodando (`python main.py`), testes verdes e as queries.
- **README** com: o que o projeto faz, como rodar, e um resumo dos achados.
- Um parágrafo **Situação → Ação → Resultado** para o currículo (ver M15).

## 📊 Rubrica (0–100)
| Critério | Peso |
|---|---|
| Corretude (pipeline roda, resultados certos) | 30 |
| Qualidade de código (funções puras, nomes, estrutura) | 25 |
| Robustez (trata dados sujos, reproduzível) | 15 |
| Testes (`pytest` cobrindo a transformação) | 15 |
| Documentação (README claro, reprodutível) | 15 |

Conceito mínimo para "concluído": **60**, sem nenhum critério zerado.

## 💡 Dicas (hint ladder)
:::{dropdown} Dica 1 — estrutura
Separe `ingest.py` / `transform.py` / `load.py` e um `main.py` que os compõe (como o `Pipeline` do M3 U2).
:::
:::{dropdown} Dica 2 — reprodutibilidade
Na carga, use `CREATE OR REPLACE TABLE` (DuckDB) para rodar de novo sem duplicar.
:::
:::{dropdown} Dica 3 — dados sujos
O `valor` vem como texto/None em algumas linhas; converta com tratamento de erro (quarentena, M3 U3) antes de calcular a receita.
:::

## 🚀 Como publicar (build-in-public)
```bash
cd projetos/eixo-1-fundamentos/starter
git init && git add -A && git commit -m "feat: pipeline do projeto integrador do Eixo 1"
# crie um repo no GitHub e:
git remote add origin https://github.com/SEU-USUARIO/pipeline-pedidos.git
git push -u origin main
```

Ponto de partida (esqueleto, testes e dados): pasta `starter/` (comece pelo seu `README.md`).

---
**Revisado em:** 2026-08-22
