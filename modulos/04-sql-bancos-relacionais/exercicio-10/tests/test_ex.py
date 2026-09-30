"""Testes do Exercício 10 (M4). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE logs(id INT, nivel VARCHAR)')
    c.executemany('INSERT INTO logs VALUES (?,?)', [(1, 'INFO'), (2, 'ERROR'), (3, 'INFO'), (4, 'ERROR'), (5, 'WARN')])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [('ERROR', 2), ('INFO', 2), ('WARN', 1)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [(2,)]


# ---------- armadilhas: as MESMAS queries numa base com casos de borda ----------
# nivel NULL vira um grupo próprio no GROUP BY; 'error' minúsculo NÃO é 'ERROR'.
@pytest.fixture
def con_bordas(con):
    con.executemany("INSERT INTO logs VALUES (?,?)", [
        (6, None),
        (7, 'error'),
        (8, 'ERROR'),
        (9, None),
    ])
    return con


def test_a_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_A).fetchall() == [('ERROR', 3), ('INFO', 2), ('WARN', 1), ('error', 1), (None, 2)]


def test_b_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_B).fetchall() == [(3,)]
