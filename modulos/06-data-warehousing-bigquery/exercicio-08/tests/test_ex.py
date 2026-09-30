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


# ---------- armadilhas: as MESMAS queries numa base com casos de borda ----------
# Fronteiras do intervalo: 31/01 é janeiro, 01/02 já é fevereiro, 31/12/2025 e 01/03/2026 ficam fora.
@pytest.fixture
def con_bordas(con):
    con.executemany("INSERT INTO eventos VALUES (?,?,?)", [
        ('2026-01-31', 'x', 1),
        ('2026-02-01', 'y', 2),
        ('2025-12-31', 'x', 100),
        ('2026-03-01', 'y', 100),
    ])
    return con


def test_a_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_A).fetchall() == [('x', 11), ('y', 20)]


def test_b_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_B).fetchall() == [('x', 30), ('y', 42)]
