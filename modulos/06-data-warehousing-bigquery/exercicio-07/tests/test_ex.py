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


# ---------- armadilhas: as MESMAS queries numa base com casos de borda ----------
# Outro ano na categoria A e um mês de 2025 (da categoria B) que passa a ser o de maior receita.
@pytest.fixture
def con_bordas(con):
    con.executemany("INSERT INTO fato_vendas VALUES (?,?,?,?)", [
        (2023, 1, 'A', 5),
        (2025, 4, 'B', 400),
    ])
    return con


def test_a_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_A).fetchall() == [(2023, 5), (2024, 100), (2025, 550)]


def test_b_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_B).fetchall() == [(4, 400)]
