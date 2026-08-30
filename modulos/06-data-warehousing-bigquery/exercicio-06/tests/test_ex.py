"""Testes do Exercício 06 (M6). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

DADOS = [(1, 'ana', 'sp', 100), (2, 'bruno', 'RJ', 200), (1, 'ana', 'sp', 100), (3, 'caio', 'mg', 50), (4, 'diana', 'SP', 80)]

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE raw_pedidos(pedido_id INTEGER, cliente VARCHAR, estado VARCHAR, valor INTEGER)')
    c.executemany('INSERT INTO raw_pedidos VALUES (?,?,?,?)', DADOS)
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [(1, 'ana', 'SP', 100), (2, 'bruno', 'RJ', 200), (3, 'caio', 'MG', 50), (4, 'diana', 'SP', 80)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [('MG', 1), ('RJ', 1), ('SP', 2)]
