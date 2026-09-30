"""Testes do Exercício 08 (M4). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE vendas(vendedor VARCHAR, valor INT)')
    c.executemany('INSERT INTO vendas VALUES (?,?)', [('ana', 100), ('ana', 200), ('bruno', 50), ('caio', 300)])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [('ana', 300), ('caio', 300), ('bruno', 50)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [('ana',), ('caio',)]


# ---------- armadilhas: as MESMAS queries numa base com casos de borda ----------
# outra distribuição de vendas: muda quem fica acima da média (resultado decorado não passa).
@pytest.fixture
def con_bordas(con):
    con.executemany("INSERT INTO vendas VALUES (?,?)", [
        ('duda', 900),
        ('bruno', 400),
        ('eva', 10),
    ])
    return con


def test_a_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_A).fetchall() == [('duda', 900), ('bruno', 450), ('ana', 300), ('caio', 300), ('eva', 10)]


def test_b_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_B).fetchall() == [('bruno',), ('duda',)]
