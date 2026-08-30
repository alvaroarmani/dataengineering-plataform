"""Testes do Exercício 11 (M4). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE pagamentos(pedido_id INT, valor INT)')
    c.executemany('INSERT INTO pagamentos VALUES (?,?)', [(1, 100), (2, 200), (1, 100), (3, 50), (2, 200)])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [(1,), (2,)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [(5, 3)]
