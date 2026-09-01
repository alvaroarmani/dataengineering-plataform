# Star Schema + dbt — Projeto Integrador do Eixo 2

Modela dimensionalmente um mini-dataset de e-commerce (**star schema**: 1 fato + dimensões,
com **SCD Tipo 2**) e implementa as transformações — primeiro em pandas (auto-corrigível, roda
em qualquer lugar), depois em **dbt** sobre a bancada Postgres (a trilha real, M07).

## Trilha A — núcleo auto-corrigível (comece aqui)
```bash
python -m venv .venv && source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q            # implemente modelagem.py até os 4 testes passarem
```
Você implementa em `modelagem.py`:
- `construir_dim_produto` — dimensão com **chave substituta** (surrogate key).
- `construir_fct_vendas` — fato no **grão** de pedido, com FK substituta e `receita`.
- `aplicar_scd2` — dimensão **SCD Tipo 2** (valido_de / valido_ate / is_current).

## Trilha B — a versão real em dbt (bancada) 🐳
Reproduza o mesmo modelo em **dbt sobre Postgres** (como no M07):
```bash
cd ../../../ambiente && docker compose up -d
docker compose --profile dbt run --rm dbt build \
  --project-dir  projetos/eixo-2-datawarehousing/starter/dbt \
  --profiles-dir projetos/eixo-2-datawarehousing/starter/dbt
```
Complete os models em `dbt/models/` (staging → marts) e o snapshot SCD2 em `dbt/snapshots/`,
com testes `unique`/`not_null`/`relationships` no `schema.yml`.

## Estrutura
```
starter/
├── modelagem.py          # trilha A — VOCÊ implementa (3 funções)
├── data/                 # seeds (produtos, pedidos, histórico p/ SCD2)
├── tests/test_modelagem.py
├── dbt/                  # trilha B — projeto dbt (staging/marts/snapshot) a completar
└── requirements.txt
```

## Entregáveis
- Repositório **GitHub** com as 4 checagens verdes (trilha A) e, idealmente, a trilha B em dbt.
- **README** com o diagrama do star schema (mermaid), como rodar e os achados.
- Parágrafo **Situação → Ação → Resultado** para o currículo (M15).
