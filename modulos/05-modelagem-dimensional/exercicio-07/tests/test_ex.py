"""Testes do Exercício 07 (M5). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE dim_cliente(sk INT, cliente_id INT, cidade VARCHAR, valido_de DATE, valido_ate DATE, corrente BOOLEAN)')
    c.executemany('INSERT INTO dim_cliente VALUES (?,?,?,?,?,?)', [(1, 100, 'SP', '2024-01-01', '2025-06-01', False), (2, 100, 'RJ', '2025-06-01', '9999-12-31', True), (3, 200, 'MG', '2024-03-01', '9999-12-31', True)])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [(100, 'RJ'), (200, 'MG')]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [(100, 'SP'), (200, 'MG')]
