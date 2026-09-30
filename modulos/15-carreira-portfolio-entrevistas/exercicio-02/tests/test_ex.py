import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import escolher_projetos  # noqa: E402


def p(nome, foco, readme=80, commits=40, ultimo="2026-08-01", dados=True, testes=True, ci=True, demo=False):
    return {"nome": nome, "foco": foco, "readme_nota": readme, "commits": commits, "ultimo_commit": ultimo,
            "dados_reais": dados, "testes": testes, "ci": ci, "demo": demo}


PROJETOS = [
    p("pipeline-olist", "modelagem", readme=95, demo=True),
    p("dbt-nyc-taxi", "modelagem", readme=90),
    p("kafka-cliques", "streaming", readme=70, ci=False),
    p("airflow-bcb", "orquestracao", readme=85, testes=False),
    p("tutorial-pandas", "analise", readme=40),                        # README fraco
    p("tcc-dw", "modelagem", readme=100, ultimo="2025-06-01", demo=True),  # parado há mais de 1 ano
    p("hello-spark", "processamento", commits=2),                       # só 2 commits
]


def test_escolha_com_diversidade():
    assert escolher_projetos(PROJETOS, "2026-09-30") == [
        ("pipeline-olist", 11.85), ("airflow-bcb", 7.55), ("kafka-cliques", 7.1)]


def test_sem_diversidade_suficiente_completa_com_os_melhores():
    assert escolher_projetos(PROJETOS[:2], "2026-09-30", n=3) == [("pipeline-olist", 11.85), ("dbt-nyc-taxi", 9.7)]


def test_eliminatorios():
    nomes = [n for n, _ in escolher_projetos(PROJETOS, "2026-09-30", n=10)]
    assert "tutorial-pandas" not in nomes and "tcc-dw" not in nomes and "hello-spark" not in nomes
    assert nomes == ["pipeline-olist", "airflow-bcb", "kafka-cliques", "dbt-nyc-taxi"]
    assert escolher_projetos(PROJETOS, "2026-09-30", n=1) == [("pipeline-olist", 11.85)]
