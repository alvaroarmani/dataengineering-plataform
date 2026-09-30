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


# ---------- armadilhas: as MESMAS queries numa base com casos de borda ----------
# EMPATE de valor (id 3 e id 5 valem 80) — o ROW_NUMBER desempata pelo menor id.
@pytest.fixture
def con_bordas(con):
    con.executemany("INSERT INTO itens VALUES (?,?)", [
        (5, 80),
        (6, 0),
    ])
    return con


def test_a_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_A).fetchall() == [(3, 1), (5, 2), (1, 3), (2, 4), (4, 5), (6, 6)]


def test_b_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_B).fetchall() == [(1, 50), (2, 80), (3, 160), (4, 170), (5, 250), (6, 250)]
