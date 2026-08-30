# Etapa 3 — Ingestão reproduzível e transformação com dbt

> Semanas ~3–4. Objetivo: dados **carregados** na camada raw e **transformados** em staging→marts
> com **dbt**, tudo com **testes verdes** e docs. É o miolo do ELT.

## 🎯 O que entregar nesta etapa
- Script de ingestão reproduzível (CSV Olist → tabelas `raw`).
- Projeto dbt com camadas `staging` → `marts` implementando o modelo da Etapa 2.
- Testes dbt (`unique`, `not_null`, `relationships`) passando.
- `dbt docs` gerando catálogo + lineage.

## 1. Ingestão → raw (bronze)
Escreva um script Python (em `ingestao/`) que carrega os CSVs do Olist para o schema `raw` do
Postgres. Requisitos:
- **Reproduzível:** rodar do zero recria as tabelas raw.
- **Idempotente:** rodar de novo não duplica (ex.: `TRUNCATE`/replace por tabela, ou `COPY` para
  tabela recriada).
- Sem transformação aqui — raw é fiel à fonte (M08: landing zone / bronze).

## 2. Staging (silver) — limpeza e padronização
No dbt, um model `stg_*` por fonte:
- Renomeia colunas para um padrão (snake_case), tipa, remove duplicatas óbvias.
- 1 staging por tabela de origem; nada de joins pesados ainda.
- Materialização `view` costuma bastar aqui.

## 3. Marts (gold) — o star schema
Implemente as dimensões e a fato da Etapa 2 como models `dim_*` e `fct_*`:
- `dim_*`: surrogate keys, atributos descritivos limpos; a dimensão SCD2 via **snapshot** dbt.
- `fct_pedidos`: joins das staging, FKs para as dimensões, medidas calculadas.
- Materialização `table` (ou `incremental` se quiser praticar M08).

## 4. Testes e docs (o que separa amador de profissional)
No `schema.yml` de cada model, declare testes:
- `not_null` e `unique` nas chaves.
- `relationships` da fato para cada dimensão (integridade referencial).
- Testes de negócio quando fizer sentido (ex.: `valor >= 0` com `dbt_utils`/`accepted_range`).

Rode:
```bash
dbt build      # roda models + testes
dbt test       # só os testes
dbt docs generate && dbt docs serve   # catálogo + lineage
```
Um `dbt build` **verde** é um entregável obrigatório do TCC.

## 5. Ligação com as perguntas de negócio
Para cada pergunta da Etapa 1, escreva a query analítica que a responde a partir dos marts
(guarde em `dbt/analises/` ou no relatório). Se alguma pergunta não é respondível, **volte ao
modelo** — é para isso que serve validar cedo.

## ✅ Checklist de saída (Etapa 3)
- [ ] Ingestão raw reproduzível e idempotente.
- [ ] Staging + marts implementando o modelo da Etapa 2.
- [ ] SCD2 via snapshot dbt.
- [ ] `dbt build` verde (models + testes).
- [ ] `dbt docs` com lineage; queries que respondem as perguntas de negócio.

## 🎤 Use a IA como banca
*"Meus testes dbt cobrem as chaves e as relações. Que teste de qualidade de dados eu ainda
deveria adicionar para as perguntas de negócio que prometi responder?"*

---
**Revisado em:** 2026-08-30
