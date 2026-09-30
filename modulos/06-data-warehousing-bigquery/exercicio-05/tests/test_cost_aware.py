"""Testes do Exercício 05 (M6). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

FATO = [
    (2025, 1, "A", 300, "x"),
    (2025, 1, "B", 150, "x"),
    (2025, 2, "A", 250, "x"),
    (2024, 1, "A", 100, "x"),
]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE fato(ano INT, mes INT, categoria VARCHAR, price INT, descricao VARCHAR)")
    c.executemany("INSERT INTO fato VALUES (?,?,?,?,?)", FATO)
    return c


def test_receita_por_categoria_2025(con):
    # 2025: A = 300 + 250 = 550, B = 150
    assert con.execute(CONSULTA_A).fetchall() == [("A", 550), ("B", 150)]


def test_mes_maior_receita_2025(con):
    # 2025: mes 1 = 450, mes 2 = 250 -> maior é mes 1
    assert con.execute(CONSULTA_B).fetchall() == [(1, 450)]


# ---------- armadilhas: as MESMAS queries numa base com casos de borda ----------
# Um mês novo vira o campeão de 2025 e um valor enorme em 2024 pune quem esquece o filtro de partição.
@pytest.fixture
def con_bordas(con):
    con.executemany("INSERT INTO fato VALUES (?,?,?,?,?)", [
        (2025, 3, 'C', 600, 'x'),
        (2024, 5, 'A', 9999, 'x'),
    ])
    return con


def test_a_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_A).fetchall() == [('C', 600), ('A', 550), ('B', 150)]


def test_b_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_B).fetchall() == [(3, 600)]
