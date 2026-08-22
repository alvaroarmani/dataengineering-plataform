"""Testes do Exercício 01 (M4). Faça todos passarem: pytest -q

As queries do aluno rodam contra uma tabela DuckDB em memória.
"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

ROWS = [
    (1, "SP", "eletronicos", 1200.0, 1), (2, "SP", "livros", 50.0, 2),
    (3, "RJ", "livros", 30.0, 1), (4, "MG", "casa", 80.0, 3),
    (5, "SP", "eletronicos", 800.0, 2), (6, "RJ", "casa", 150.0, 4),
    (7, "SP", "livros", 45.0, 1), (8, "MG", "eletronicos", 600.0, 3),
    (9, "RJ", "eletronicos", 900.0, 2), (10, "SP", "casa", 200.0, 5),
    (11, "MG", "livros", 25.0, 4), (12, "SP", "eletronicos", 1500.0, 1),
    (13, "RJ", "livros", 60.0, 5), (14, "MG", "casa", 120.0, 3),
    (15, "SP", "livros", 40.0, 2),
]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute(
        "CREATE TABLE pedidos(id INTEGER, estado VARCHAR, categoria VARCHAR, "
        "valor DOUBLE, cliente_id INTEGER)"
    )
    c.executemany("INSERT INTO pedidos VALUES (?,?,?,?,?)", ROWS)
    return c


def test_consulta_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [
        (12, 1500.0), (1, 1200.0), (5, 800.0), (10, 200.0),
    ]


def test_consulta_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [
        ("eletronicos", 5000.0), ("casa", 550.0), ("livros", 250.0),
    ]
