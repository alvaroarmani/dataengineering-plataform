# Etapa 4 — Orquestração, empacotamento, documentação e defesa

> Semanas ~5–6. Objetivo: o pipeline **orquestrado** por Airflow, tudo **empacotado** em
> docker-compose, **documentado** para reprodutibilidade e **defendido** em vídeo. É a entrega final.

## 🎯 O que entregar nesta etapa
- Uma DAG Airflow que roda o pipeline fim a fim (ingestão → dbt), agendada e idempotente.
- `docker-compose.yml` que sobe o stack completo.
- README completo + ADRs + relatório (6–12 págs).
- Vídeo de defesa (5–10 min) e repositório público reproduzível.

## 1. Orquestração com Airflow (M09)
Modele o pipeline como uma DAG (`airflow/dags/pipeline_dw.py`):
- Tarefas: `ingestao_raw` → `dbt_build` (→ `dbt_test` se separado) → (opcional) `checagens_qualidade`.
- **Dependências** explícitas (a fato depois das dimensões, garantido pelo dbt).
- **Agendamento** (`schedule`) e `catchup=False` para começar.
- **Idempotência:** rerodar uma data não duplica dados (reprocessa por partição/replace).
- **Tratamento de falha:** `retries`, e um alerta/log em caso de erro.

Valide sem scheduler:
```bash
airflow dags test pipeline_dw 2024-01-01
```

## 2. Empacotamento com docker-compose (M10)
O `docker-compose.yml` deve subir tudo o que um terceiro precisa: Postgres, Airflow (e dbt via
container ou dentro do Airflow). Meta: **`docker compose up` e o projeto funciona** — sem
"instale X na sua máquina". Fixe versões (tags) para reprodutibilidade.

## 3. Verificações de qualidade e observabilidade (M12)
- Os testes dbt já cobrem qualidade estrutural; adicione ao menos uma checagem de negócio.
- Observabilidade mínima: logs da DAG legíveis e uma forma de saber se a última execução passou.

## 4. Documentação (metade da nota — leve a sério)
- **README** completo: o quê, por quê (perguntas de negócio), **arquitetura (diagrama mermaid)**,
  **como rodar** (`docker compose up` + passos), e o que você aprendeu.
- **ADRs** em `docs/decisoes/`: armazenamento, escolha de grão, qual dimensão é SCD2, etc.
- **Relatório** (6–12 págs): problema, arquitetura, modelagem, decisões, resultados (respostas às
  perguntas de negócio), limitações e próximos passos.

## 5. Defesa (arguição)
Grave 5–10 min mostrando: o problema, a arquitetura, uma execução do pipeline, e as perguntas de
negócio respondidas. Antes, faça um **mock** usando a IA como banca (M15): peça que critique suas
decisões de grão, idempotência e testes.

## ✅ Checklist de entrega final (rubrica do TCC)
- [ ] DAG Airflow fim a fim, agendada, idempotente, com tratamento de falha.
- [ ] `docker compose up` sobe o stack completo (reprodutível por um terceiro).
- [ ] `dbt build` verde (models + testes) e `dbt docs` com lineage.
- [ ] Modelo dimensional com SCD2, respondendo as perguntas de negócio.
- [ ] README + ADRs + relatório (6–12 págs) + vídeo (5–10 min).
- [ ] Repositório público no GitHub, limpo (sem dados grandes versionados, sem segredos — M14).

## 🎤 Use a IA como banca (mock final)
*"Aja como uma banca crítica de TCC de Engenharia de Dados. Questione minhas escolhas de grão,
idempotência da DAG, cobertura de testes e reprodutibilidade. Onde meu projeto é mais frágil?"*

> **Parabéns:** ao fechar este checklist você concluiu a especialização — e tem, no GitHub, a
> prova de que constrói uma plataforma de dados de ponta a ponta.

---
**Revisado em:** 2026-08-30
