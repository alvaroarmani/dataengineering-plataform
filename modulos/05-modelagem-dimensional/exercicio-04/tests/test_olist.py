"""Testes do Exercício 04 (M5). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

CLIENTES = [(1, "c1", "SP"), (2, "c2", "RJ"), (3, "c3", "MG")]
PRODUTOS = [(1, "p1", "cama_mesa_banho"), (2, "p2", "informatica_acessorios"), (3, "p3", "moveis_decoracao")]
# (sk_cliente, sk_produto, price, freight)
FATO = [
    (1, 1, 50.0, 10.0), (1, 2, 200.0, 15.0), (2, 1, 60.0, 12.0), (2, 3, 300.0, 40.0),
    (3, 2, 180.0, 20.0), (1, 1, 70.0, 11.0), (3, 3, 250.0, 35.0), (2, 2, 220.0, 18.0),
]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE dim_cliente(sk_cliente INT, customer_id VARCHAR, estado VARCHAR)")
    c.executemany("INSERT INTO dim_cliente VALUES (?,?,?)", CLIENTES)
    c.execute("CREATE TABLE dim_produto(sk_produto INT, product_id VARCHAR, categoria VARCHAR)")
    c.executemany("INSERT INTO dim_produto VALUES (?,?,?)", PRODUTOS)
    c.execute("CREATE TABLE fato_item_pedido(sk_cliente INT, sk_produto INT, price DOUBLE, freight DOUBLE)")
    c.executemany("INSERT INTO fato_item_pedido VALUES (?,?,?,?)", FATO)
    return c


def test_ticket_medio_por_categoria(con):
    # cama_mesa_banho: (50,60,70)->60 ; informatica: (200,180,220)->200 ; moveis: (300,250)->275
    assert con.execute(CONSULTA_A).fetchall() == [
        ("moveis_decoracao", 275.0),
        ("informatica_acessorios", 200.0),
        ("cama_mesa_banho", 60.0),
    ]


def test_receita_total_por_estado(con):
    # SP: 60+215+81=356 ; RJ: 72+340+238=650 ; MG: 200+285=485
    assert con.execute(CONSULTA_B).fetchall() == [
        ("RJ", 650.0),
        ("MG", 485.0),
        ("SP", 356.0),
    ]
