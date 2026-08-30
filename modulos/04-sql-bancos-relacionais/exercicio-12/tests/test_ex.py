"""Testes do Exercício 12 (M4). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE contas(conta VARCHAR, saldo INT)')
    c.executemany('INSERT INTO contas VALUES (?,?)', [('a', 100), ('b', -20), ('c', 50), ('d', -5)])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [('b',), ('d',)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [(150,)]
