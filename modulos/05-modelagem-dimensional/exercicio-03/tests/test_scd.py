"""Testes do Exercício 03 (M5). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

LINHAS = [
    (1, 100, "São Paulo", "2024-01-01", "2025-03-01", False),
    (2, 100, "Campinas", "2025-03-01", "9999-12-31", True),
    (3, 200, "Rio de Janeiro", "2024-06-01", "9999-12-31", True),
    (4, 300, "Curitiba", "2024-02-01", "2024-11-01", False),
    (5, 300, "Belo Horizonte", "2024-11-01", "9999-12-31", True),
]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute(
        "CREATE TABLE dim_cliente(sk INT, cliente_id INT, cidade VARCHAR, "
        "valido_de DATE, valido_ate DATE, corrente BOOLEAN)"
    )
    c.executemany("INSERT INTO dim_cliente VALUES (?,?,?,?,?,?)", LINHAS)
    return c


def test_visao_atual(con):
    assert con.execute(CONSULTA_A).fetchall() == [
        (100, "Campinas"),
        (200, "Rio de Janeiro"),
        (300, "Belo Horizonte"),
    ]


def test_point_in_time(con):
    # Em 2024-07-01: cliente 100=São Paulo, 200=Rio de Janeiro, 300=Curitiba
    assert con.execute(CONSULTA_B).fetchall() == [
        (100, "São Paulo"),
        (200, "Rio de Janeiro"),
        (300, "Curitiba"),
    ]
