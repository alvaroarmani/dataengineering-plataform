"""Testes do Exercício 04 (M7). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

ITENS = [(1, "p1", 100.0), (2, "p2", 200.0), (3, "p1", 50.0), (4, "p3", 80.0)]
PRODUTOS = [("p1", "eletronicos"), ("p2", "livros"), ("p3", "casa")]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE stg_itens(item_id INT, produto_id VARCHAR, price DOUBLE)")
    c.executemany("INSERT INTO stg_itens VALUES (?,?,?)", ITENS)
    c.execute("CREATE TABLE stg_produtos(produto_id VARCHAR, categoria VARCHAR)")
    c.executemany("INSERT INTO stg_produtos VALUES (?,?)", PRODUTOS)
    return c


def test_receita_por_categoria(con):
    assert con.execute(CONSULTA_A).fetchall() == [
        ("livros", 200.0),
        ("eletronicos", 150.0),
        ("casa", 80.0),
    ]


def test_ticket_medio_por_categoria(con):
    # eletronicos = avg(100,50)=75, livros=200, casa=80
    assert con.execute(CONSULTA_B).fetchall() == [
        ("livros", 200.0),
        ("casa", 80.0),
        ("eletronicos", 75.0),
    ]
