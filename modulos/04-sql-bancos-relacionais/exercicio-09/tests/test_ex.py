"""Testes do Exercício 09 (M4). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE itens(id INT, valor INT)')
    c.executemany('INSERT INTO itens VALUES (?,?)', [(1, 50), (2, 30), (3, 80), (4, 10)])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [(3, 1), (1, 2), (2, 3), (4, 4)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [(1, 50), (2, 80), (3, 160), (4, 170)]
