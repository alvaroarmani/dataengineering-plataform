import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import TIB, maiores_ofensores, ratear_custos  # noqa: E402

CONSULTAS = [
    {"id": "q1", "time": "bi", "bytes": 2 * TIB},
    {"id": "q2", "time": "bi", "bytes": TIB // 2},
    {"id": "q3", "time": "ciencia", "bytes": 4 * TIB},
    {"id": "q4", "time": None, "bytes": TIB},
    {"id": "q5", "time": "eng", "bytes": TIB // 10},
    {"id": "q6", "time": "", "bytes": 0},
]


def test_rateio_por_time():
    assert ratear_custos(CONSULTAS, 5.0) == {
        "ciencia": {"custo": 20.0, "pct": 52.6},
        "bi": {"custo": 12.5, "pct": 32.9},
        "sem_dono": {"custo": 5.0, "pct": 13.2},
        "eng": {"custo": 0.5, "pct": 1.3},
    }


def test_ordem_das_chaves_e_por_custo():
    assert list(ratear_custos(CONSULTAS, 5.0)) == ["ciencia", "bi", "sem_dono", "eng"]


def test_maiores_ofensores():
    assert maiores_ofensores(CONSULTAS, 5.0) == [("q3", "ciencia", 20.0), ("q1", "bi", 10.0), ("q4", "sem_dono", 5.0)]
    assert maiores_ofensores(CONSULTAS, 5.0, n=1) == [("q3", "ciencia", 20.0)]


def test_empate_e_vazio():
    empate = [{"id": "b", "time": "x", "bytes": TIB}, {"id": "a", "time": "y", "bytes": TIB}]
    assert [q for q, _, _ in maiores_ofensores(empate, 1.0)] == ["a", "b"]
    assert list(ratear_custos(empate, 1.0)) == ["x", "y"]
    assert ratear_custos([], 5.0) == {}
