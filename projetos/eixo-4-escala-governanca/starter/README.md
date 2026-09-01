# Processamento em escala + qualidade + CI — Projeto Integrador do Eixo 4

Processa um dataset de corridas (estilo NYC Taxi): **limpa**, **agrega** e grava em **Parquet**
(colunar), com **testes de qualidade** e **CI** — primeiro em pandas (auto-corrigível), depois
em **PySpark** gravando no **MinIO** (a trilha real, M11).

## Trilha A — núcleo auto-corrigível (comece aqui)
```bash
python -m venv .venv && source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q            # implemente processamento.py até os 3 testes passarem
```
Você implementa em `processamento.py`:
- `transformar` — calcula duração, deriva a data, **remove corridas inválidas**.
- `agregar_por_dia` — corridas, receita e duração média por dia (chave de partição).
- `escrever_parquet` — grava colunar (Parquet).

## Trilha B — em PySpark, no MinIO 🐳
Reescreva a transformação/agregação em **PySpark** (`spark/job_spark.py`) e grave **particionado
por data** em Parquet no **MinIO** (S3 local), como no [M11](../../modulos/11-spark-lakehouse/index.md):
```bash
cd ../../../ambiente && docker compose --profile spark up -d
# submeta o job no container spark (ver M11)
```

## CI (governança de qualidade)
`.github/workflows/ci.yml` roda os testes a cada push — o **portão automático** que impede
regressões (M13). **Nota de governança/LGPD (M14):** identifique no README quais campos seriam
**dados pessoais** num dataset real de corridas (ex.: identificador do passageiro, GPS) e como
você os trataria (mascaramento/retenção).

## Estrutura
```
starter/
├── processamento.py         # trilha A — VOCÊ implementa (3 funções)
├── data/amostra_corridas.csv
├── tests/test_processamento.py
├── spark/job_spark.py       # trilha B — PySpark -> MinIO (a completar)
├── .github/workflows/ci.yml # CI que roda os testes
└── requirements.txt
```

## Entregáveis
- Repositório **GitHub** com a **trilha A verde**, **CI ativo** e, idealmente, o job **PySpark** (trilha B).
- **README** com diagrama, como rodar, achados e a **nota de governança/LGPD**.
- Parágrafo **Situação → Ação → Resultado** para o currículo (M15).
