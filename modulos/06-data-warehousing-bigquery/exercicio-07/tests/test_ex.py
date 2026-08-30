"""Testes do Exercício 07 (M6). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

DADOS = [(2024, 1, 'A', 100), (2024, 2, 'B', 200), (2025, 1, 'A', 300), (2025, 2, 'B', 150), (2025, 3, 'A', 250)]

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE fato_vendas(ano INTEGER, mes INTEGER, categoria VARCHAR, valor INTEGER)')
    c.executemany('INSERT INTO fato_vendas VALUES (?,?,?,?)', DADOS)
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [(2024, 100), (2025, 550)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [(1, 300)]
