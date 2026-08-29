"""Grader do Exercício 03 (M7) — confere o mart `fct_receita_categoria` (dbt).

Pré-requisito: `dbt build` na bancada (ver enunciado). Os testes de schema do dbt
(not_null/unique) cobrem integridade; aqui checamos os VALORES da agregação.
"""
import pytest


def test_receita_por_categoria(pg):
    cur = pg.cursor()
    try:
        cur.execute(
            "SELECT categoria, receita FROM fct_receita_categoria ORDER BY receita DESC"
        )
    except Exception as e:  # noqa: BLE001
        pg.rollback()
        pytest.skip(f"fct_receita_categoria não encontrado ({e}). Rode `dbt build` primeiro.")
    rows = [(r[0], float(r[1])) for r in cur.fetchall()]
    assert rows == [
        ("livros", 200.0),
        ("eletronicos", 150.0),
        ("casa", 80.0),
    ]
