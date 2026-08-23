"""Testes do Exercício 01 (M5). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

FATO = [
    (1, 1, 10, 1, 1200.0), (2, 2, 20, 2, 50.0), (3, 1, 20, 1, 30.0), (4, 3, 30, 1, 80.0),
    (5, 2, 10, 1, 800.0), (6, 1, 10, 1, 1500.0), (7, 3, 20, 4, 35.0), (8, 2, 30, 1, 110.0),
]
CLIENTES = [(1, "ana", "São Paulo"), (2, "bruno", "Rio de Janeiro"), (3, "caio", "Belo Horizonte")]
PRODUTOS = [(10, "eletronicos"), (20, "livros"), (30, "casa")]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE dim_cliente(cliente_id INT, nome VARCHAR, cidade VARCHAR)")
    c.executemany("INSERT INTO dim_cliente VALUES (?,?,?)", CLIENTES)
    c.execute("CREATE TABLE dim_produto(produto_id INT, categoria VARCHAR)")
    c.executemany("INSERT INTO dim_produto VALUES (?,?)", PRODUTOS)
    c.execute("CREATE TABLE fato_vendas(venda_id INT, cliente_id INT, produto_id INT, quantidade INT, valor DOUBLE)")
    c.executemany("INSERT INTO fato_vendas VALUES (?,?,?,?,?)", FATO)
    return c


def test_receita_por_categoria(con):
    assert con.execute(CONSULTA_A).fetchall() == [
        ("eletronicos", 3500.0), ("casa", 190.0), ("livros", 115.0),
    ]


def test_receita_por_cliente(con):
    assert con.execute(CONSULTA_B).fetchall() == [
        ("ana", 2730.0), ("bruno", 960.0), ("caio", 115.0),
    ]
