"""Testes do Exercício 01 (M6). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

RAW = [
    (1, "ana", "sp", 100.0),
    (2, "bruno", "RJ", 200.0),
    (1, "ana", "sp", 100.0),   # duplicata
    (3, "caio", "mg", 50.0),
    (4, "ana", "SP", 80.0),
]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE raw_pedidos(pedido_id INT, cliente VARCHAR, estado VARCHAR, valor DOUBLE)")
    c.executemany("INSERT INTO raw_pedidos VALUES (?,?,?,?)", RAW)
    return c


def test_core_limpo(con):
    assert con.execute(CONSULTA_A).fetchall() == [
        (1, "ana", "SP", 100.0),
        (2, "bruno", "RJ", 200.0),
        (3, "caio", "MG", 50.0),
        (4, "ana", "SP", 80.0),
    ]


def test_mart_receita_por_estado(con):
    # com dedup: SP = 100 + 80 = 180 (não 280), RJ = 200, MG = 50
    assert con.execute(CONSULTA_B).fetchall() == [
        ("RJ", 200.0),
        ("SP", 180.0),
        ("MG", 50.0),
    ]
