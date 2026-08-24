"""Testes do Exercício 02 (M6). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

FATO = [
    (2023, 12, "B", 50.0),
    (2024, 1, "A", 100.0),
    (2024, 2, "B", 200.0),
    (2025, 1, "A", 300.0),
    (2025, 1, "B", 150.0),
    (2025, 2, "A", 250.0),
]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE fato_vendas(ano INT, mes INT, categoria VARCHAR, valor DOUBLE)")
    c.executemany("INSERT INTO fato_vendas VALUES (?,?,?,?)", FATO)
    return c


def test_pruning_categoria_2025(con):
    # 2025: A = 300 + 250 = 550, B = 150
    assert con.execute(CONSULTA_A).fetchall() == [("A", 550.0), ("B", 150.0)]


def test_range_por_ano(con):
    # ano >= 2024: 2024 = 300, 2025 = 700
    assert con.execute(CONSULTA_B).fetchall() == [(2024, 300.0), (2025, 700.0)]
