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


# ---------- armadilhas: as MESMAS queries numa base com casos de borda ----------
# A mesma reentrega com o estado escrito de jeitos diferentes ('Sp', ' sp ') — só vira UMA linha se você padronizar com TRIM + UPPER ANTES de deduplicar.
@pytest.fixture
def con_bordas(con):
    con.executemany("INSERT INTO raw_pedidos VALUES (?,?,?,?)", [
        (5, 'eva', 'Sp', 70.0),
        (5, 'eva', ' sp ', 70.0),
        (6, 'fabio', ' rj', 30.0),
    ])
    return con


def test_a_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_A).fetchall() == [(1, 'ana', 'SP', 100.0), (2, 'bruno', 'RJ', 200.0), (3, 'caio', 'MG', 50.0), (4, 'ana', 'SP', 80.0), (5, 'eva', 'SP', 70.0), (6, 'fabio', 'RJ', 30.0)]


def test_b_bordas(con_bordas):
    assert con_bordas.execute(CONSULTA_B).fetchall() == [('SP', 250.0), ('RJ', 230.0), ('MG', 50.0)]
