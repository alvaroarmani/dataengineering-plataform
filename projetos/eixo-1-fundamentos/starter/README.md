# Pipeline de Pedidos — Projeto Integrador do Eixo 1

Mini-pipeline batch: **ingere** um CSV sujo → **transforma** com pandas → **carrega** no
DuckDB → **analisa** com SQL. Junta Git + Python + SQL num entregável de portfólio.

## Como rodar
```bash
python -m venv .venv && source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q            # os testes da transformação devem passar
python main.py       # roda o pipeline completo e imprime as análises
```

## Estrutura
```
starter/
├── data/pedidos.csv          # dados de propósito sujos
├── pipeline/
│   ├── ingest.py             # ler o CSV
│   ├── transform.py          # limpar/transformar (VOCÊ implementa)
│   └── load.py               # carregar no DuckDB
├── consultas.sql             # 5 queries de análise (VOCÊ escreve)
├── tests/test_transform.py   # pytest da transformação
├── main.py                   # orquestra tudo
└── requirements.txt
```

## Sua tarefa
1. Implemente as funções em `pipeline/transform.py` (faça `pytest` passar).
2. Complete a carga em `pipeline/load.py` (reproduzível).
3. Escreva as queries em `consultas.sql`.
4. Rode `python main.py`, confira os resultados e escreva um resumo no fim deste README.

## Meus achados
_(preencha depois de rodar: 2–3 frases sobre o que os dados mostraram)_

---
Parte da [Especialização em Engenharia de Dados](../../index.md) · Eixo 1.
