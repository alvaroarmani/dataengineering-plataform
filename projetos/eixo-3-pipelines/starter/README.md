# ELT incremental de uma API — Projeto Integrador do Eixo 3

Automatiza um fluxo **ELT**: ingere cotações de câmbio de uma **API**, integra de forma
**incremental e idempotente**, aplica um **portão de qualidade** — primeiro como funções puras
(auto-corrigível), depois orquestrado por uma **DAG Airflow** na bancada.

## Trilha A — núcleo auto-corrigível (comece aqui)
```bash
python -m venv .venv && source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q            # implemente pipeline.py até os 3 testes passarem
```
Você implementa em `pipeline.py`:
- `parse_cotacoes` — normaliza a resposta da API para `[data, valor]`.
- `upsert_idempotente` — integra por `data`, sem duplicar (reprocessar é seguro).
- `checar_qualidade` — detecta datas duplicadas, valores nulos/negativos.

## Trilha B — orquestração real com Airflow 🐳
Complete a DAG em `dags/dag_cambio.py` (reaproveitando as funções puras) e rode na bancada:
```bash
docker compose up -d
docker compose exec airflow airflow dags test dag_cambio 2026-08-10
```
A DAG deve ser **agendada**, **idempotente** (reprocessar um dia não duplica) e falhar se a
qualidade não passar. API sugerida: cotação do dólar (Banco Central / PTAX) ou IBGE.

## Estrutura
```
starter/
├── pipeline.py           # trilha A — VOCÊ implementa (3 funções)
├── data/amostra_api.json # exemplo de resposta da API (fixture dos testes)
├── tests/test_pipeline.py
├── dags/dag_cambio.py    # trilha B — DAG a completar
├── docker-compose.yml    # Airflow + Postgres
└── requirements.txt
```

## Entregáveis
- Repositório **GitHub** com a **trilha A verde** e, idealmente, a **DAG rodando** (trilha B).
- **README** com o diagrama do fluxo (mermaid) e como rodar.
- Parágrafo **Situação → Ação → Resultado** para o currículo (M15).
