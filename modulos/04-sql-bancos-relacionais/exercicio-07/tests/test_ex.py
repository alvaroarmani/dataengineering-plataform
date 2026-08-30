"""Testes do Exercício 07 (M4). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE pedidos(id INT, cliente_id INT, valor INT)')
    c.executemany('INSERT INTO pedidos VALUES (?,?,?)', [(1, 1, 100), (2, 2, 200), (3, 1, 50), (4, 3, 80)])
    c.execute('CREATE TABLE clientes(id INT, nome VARCHAR, cidade VARCHAR)')
    c.executemany('INSERT INTO clientes VALUES (?,?,?)', [(1, 'ana', 'SP'), (2, 'bruno', 'RJ'), (3, 'caio', 'SP')])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [('SP', 230), ('RJ', 200)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [('bruno', 200)]
