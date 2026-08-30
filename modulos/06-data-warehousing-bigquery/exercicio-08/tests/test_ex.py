"""Testes do Exercício 08 (M6). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

DADOS = [('2026-01-05', 'x', 10), ('2026-01-20', 'y', 20), ('2026-02-10', 'x', 30), ('2026-02-15', 'y', 40)]

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE eventos(dia DATE, tipo VARCHAR, valor INTEGER)')
    c.executemany('INSERT INTO eventos VALUES (?,?,?)', DADOS)
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [('x', 10), ('y', 20)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [('x', 30), ('y', 40)]
