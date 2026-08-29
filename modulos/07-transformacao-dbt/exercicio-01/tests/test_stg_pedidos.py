"""Grader do Exercício 01 (M7) — confere o model `stg_pedidos` construído pelo dbt.

Pré-requisito: rodar `dbt build` (seed + model + testes) na bancada. Ver enunciado.
Os testes de schema do próprio dbt (not_null/unique) já cobrem parte; aqui checamos os
VALORES da transformação (estado em maiúscula, tipos convertidos).
"""
import pytest


def _rows(pg):
    cur = pg.cursor()
    try:
        cur.execute("SELECT pedido_id, cliente, estado, valor FROM stg_pedidos ORDER BY pedido_id")
    except Exception as e:  # noqa: BLE001
        pg.rollback()
        pytest.skip(f"stg_pedidos não encontrado ({e}). Rode `dbt build` primeiro.")
    return cur.fetchall()


def test_stg_pedidos_transformacao(pg):
    rows = [(r[0], r[1], r[2], float(r[3])) for r in _rows(pg)]
    assert rows == [
        (1, "ana", "SP", 100.0),
        (2, "bruno", "RJ", 200.0),
        (3, "caio", "MG", 50.0),
        (4, "ana", "SP", 80.0),
    ]


def test_pedido_id_unico(pg):
    cur = pg.cursor()
    try:
        cur.execute("SELECT COUNT(*), COUNT(DISTINCT pedido_id) FROM stg_pedidos")
    except Exception as e:  # noqa: BLE001
        pg.rollback()
        pytest.skip(f"stg_pedidos não encontrado ({e}). Rode `dbt build` primeiro.")
    total, distintos = cur.fetchone()
    assert total == distintos, "pedido_id deve ser único (grão de 1 linha por pedido)"
