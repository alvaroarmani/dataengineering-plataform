"""Testes do Exercício 03 (M15). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA  # noqa: E402

VENDAS = [
    (1, "eletronicos", 1000.0), (1, "eletronicos", 500.0),   # prod 1: 1500
    (2, "eletronicos", 800.0),                               # prod 2: 800
    (3, "eletronicos", 300.0),                               # prod 3: 300 (fora do top 2)
    (4, "livros", 120.0), (4, "livros", 30.0),               # prod 4: 150
    (5, "livros", 90.0),                                     # prod 5: 90
]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE vendas(produto_id INT, categoria VARCHAR, valor DOUBLE)")
    c.executemany("INSERT INTO vendas VALUES (?,?,?)", VENDAS)
    return c


def test_top2_por_categoria(con):
    assert con.execute(CONSULTA).fetchall() == [
        ("eletronicos", 1, 1500.0),
        ("eletronicos", 2, 800.0),
        ("livros", 4, 150.0),
        ("livros", 5, 90.0),
    ]
