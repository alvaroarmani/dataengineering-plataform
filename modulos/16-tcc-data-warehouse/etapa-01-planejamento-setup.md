# Etapa 1 — Planejamento, escopo e setup do repositório

> Semana ~1. Objetivo: sair desta etapa com o **escopo fechado**, o **repositório criado** e a
> **bancada rodando** — para nunca mais travar em "por onde começo".

## 🎯 O que entregar nesta etapa
- Repositório no GitHub criado a partir do [scaffold](../../tcc/starter/), com README inicial.
- Perguntas de negócio escolhidas (3–5) e escopo delimitado.
- Bancada Docker de pé (Postgres + serviços) e o dataset Olist baixado.
- Um ADR inicial registrando a decisão de arquitetura (Postgres local vs BigQuery).

## 1. Fixe as perguntas de negócio
Todo DW existe para **responder perguntas**. Escolha de 3 a 5 (podem vir da
[especificação](../../tcc/especificacao-dw.md)), por exemplo:
- Receita e nº de pedidos por mês, estado e categoria.
- Ticket médio e tempo médio de entrega por região.
- Taxa de reviews negativos por vendedor/categoria.
- Clientes recorrentes vs. únicos (coorte simples).

**Por quê primeiro?** As perguntas definem o grão da fato (Etapa 2) e as dimensões. Sem elas,
você modela no escuro.

## 2. Escolha a arquitetura de armazenamento
- **Postgres local** (recomendado para começar): mais simples, tudo na bancada Docker.
- **BigQuery free-tier**: mais próximo do mercado; exige projeto/credencial sua.

Registre a escolha num **ADR** (`docs/decisoes/0001-armazenamento.md` no seu repo do TCC):
contexto, decisão, consequências. Você pode desenvolver local e publicar depois uma versão em BigQuery.

## 3. Crie o repositório a partir do scaffold
O scaffold em [`tcc/starter/`](../../tcc/starter/) já traz a estrutura esperada:
```text
dw-ecommerce/
├── README.md              # o que/por quê/arquitetura/como rodar/o que aprendi
├── docker-compose.yml     # Postgres + (dbt/airflow)
├── ingestao/              # scripts de carga do Olist → raw
├── dbt/                   # projeto dbt (staging → marts)
├── airflow/dags/          # a DAG do pipeline
├── docs/decisoes/         # ADRs
└── relatorio/             # relatório final (6–12 págs)
```
Copie-o para um novo repositório, dê o primeiro commit e publique no GitHub desde já
(build in public — M15).

## 4. Suba a bancada e o dataset
- `docker compose up -d` deve subir o Postgres (e o que mais o seu compose declarar).
- Baixe o dataset **Olist** (CSV público) para `ingestao/dados/` — não versione os CSVs
  grandes (use `.gitignore`); versione o **script** que os baixa.

## ✅ Checklist de saída (Etapa 1)
- [ ] 3–5 perguntas de negócio escritas no README.
- [ ] Decisão de armazenamento registrada num ADR.
- [ ] Repositório criado do scaffold e publicado no GitHub (1º commit).
- [ ] `docker compose up` sobe a bancada sem erro.
- [ ] Dataset Olist disponível localmente (script de download versionado).

## 🎤 Use a IA como banca
Peça arguição: *"dado estas perguntas de negócio, meu escopo está coerente e viável em 60h?
Que pergunta eu deveria cortar para não estourar o prazo?"*

---
**Revisado em:** 2026-08-30
