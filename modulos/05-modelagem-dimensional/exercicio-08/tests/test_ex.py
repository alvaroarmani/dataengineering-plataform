"""Testes do Exercício 08 (M5). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE fato_item(sk_cliente INT, sk_produto INT, price INT, freight INT)')
    c.executemany('INSERT INTO fato_item VALUES (?,?,?,?)', [(1, 1, 100, 10), (1, 2, 200, 15), (2, 1, 60, 12), (2, 3, 80, 40), (3, 2, 180, 20), (1, 1, 150, 11)])
    c.execute('CREATE TABLE dim_cliente(sk_cliente INT, estado VARCHAR)')
    c.executemany('INSERT INTO dim_cliente VALUES (?,?)', [(1, 'SP'), (2, 'RJ'), (3, 'MG')])
    c.execute('CREATE TABLE dim_produto(sk_produto INT, categoria VARCHAR)')
    c.executemany('INSERT INTO dim_produto VALUES (?,?)', [(1, 'A'), (2, 'B'), (3, 'C')])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [('RJ', 52), ('SP', 36), ('MG', 20)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [('B', 190.0), ('A', 103.33333333333333), ('C', 80.0)]
