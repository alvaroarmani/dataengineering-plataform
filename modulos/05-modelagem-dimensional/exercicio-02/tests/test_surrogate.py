"""Testes do Exercício 02 (M5). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

STG_PRODUTO = [("P-100", "eletronicos"), ("P-050", "livros"), ("P-200", "casa"), ("P-010", "livros")]
STG_VENDA = [(1, "P-100", 1200.0), (2, "P-010", 30.0), (3, "P-200", 80.0), (4, "P-100", 1500.0)]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE stg_produto(codigo VARCHAR, categoria VARCHAR)")
    c.executemany("INSERT INTO stg_produto VALUES (?,?)", STG_PRODUTO)
    # dim_produto já materializada (para o lookup do item B)
    c.execute(
        "CREATE TABLE dim_produto AS "
        "SELECT ROW_NUMBER() OVER (ORDER BY codigo) AS sk_produto, codigo, categoria FROM stg_produto"
    )
    c.execute("CREATE TABLE stg_venda(venda_id INT, codigo_produto VARCHAR, valor DOUBLE)")
    c.executemany("INSERT INTO stg_venda VALUES (?,?,?)", STG_VENDA)
    return c


def test_dimensao_com_surrogate_key(con):
    # ROW_NUMBER ordenado por codigo: P-010=1, P-050=2, P-100=3, P-200=4
    assert con.execute(CONSULTA_A).fetchall() == [
        (1, "P-010", "livros"),
        (2, "P-050", "livros"),
        (3, "P-100", "eletronicos"),
        (4, "P-200", "casa"),
    ]


def test_surrogate_key_lookup_no_fato(con):
    assert con.execute(CONSULTA_B).fetchall() == [
        (1, 3, 1200.0),
        (2, 1, 30.0),
        (3, 4, 80.0),
        (4, 3, 1500.0),
    ]
