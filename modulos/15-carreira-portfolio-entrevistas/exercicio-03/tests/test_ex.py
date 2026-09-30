"""Testes do Exercício 03 (M15). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import CONSULTA  # noqa: E402

VENDAS = [
    (1, "eletronicos", 1000.0), (1, "eletronicos", 500.0),   # prod 1: 1500
    (2, "eletronicos", 800.0),                               # prod 2: 800
    (3, "eletronicos", 300.0),                               # prod 3: 300 (fora do top 2)
    (4, "livros", 120.0), (4, "livros", 30.0),               # prod 4: 150
    (5, "livros", 90.0),                                     # prod 5: 90
]


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE vendas(produto_id INT, categoria VARCHAR, valor DOUBLE)")
    c.executemany("INSERT INTO vendas VALUES (?,?,?)", VENDAS)
    return c


def test_top2_por_categoria(con):
    assert con.execute(CONSULTA).fetchall() == [
        ("eletronicos", 1, 1500.0),
        ("eletronicos", 2, 800.0),
        ("livros", 4, 150.0),
        ("livros", 5, 90.0),
    ]


# ---------- armadilhas: empate de receita e categoria com menos de 2 produtos ----------
@pytest.fixture
def con_bordas(con):
    con.executemany("INSERT INTO vendas VALUES (?,?,?)", [
        (6, "eletronicos", 800.0),       # empata com o produto 2 (800): desempate pelo menor id
        (7, "casa", 60.0),               # categoria com um produto só
        (8, "livros", None),             # venda sem valor: SUM ignora, receita nula fica por último
    ])
    return con


def test_empate_desempata_pelo_id(con_bordas):
    r = con_bordas.execute(CONSULTA).fetchall()
    assert [x for x in r if x[0] == "eletronicos"] == [("eletronicos", 1, 1500.0), ("eletronicos", 2, 800.0)]


def test_categoria_pequena_e_nulos(con_bordas):
    r = con_bordas.execute(CONSULTA).fetchall()
    assert ("casa", 7, 60.0) in r
    assert [x for x in r if x[0] == "livros"] == [("livros", 4, 150.0), ("livros", 5, 90.0)]
    assert len(r) == 5
