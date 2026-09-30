import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import agregar  # noqa: E402

LINHAS = [
    {"categoria": "livros", "valor": 30.0}, {"categoria": "livros", "valor": None},
    {"categoria": "livros", "valor": 50.0}, {"categoria": "casa", "valor": None},
    {"categoria": "casa"}, {"categoria": None, "valor": 10.0}, {"valor": 5.0},
    {"categoria": "brinquedos", "valor": 0.0},
]


def test_semantica_completa():
    assert agregar(LINHAS, "categoria", "valor") == [
        {"categoria": "brinquedos", "linhas": 1, "n": 1, "soma": 0.0, "media": 0.0, "maximo": 0.0},
        {"categoria": "casa", "linhas": 2, "n": 0, "soma": None, "media": None, "maximo": None},
        {"categoria": "livros", "linhas": 3, "n": 2, "soma": 80.0, "media": 40.0, "maximo": 50.0},
        {"categoria": None, "linhas": 2, "n": 2, "soma": 15.0, "media": 7.5, "maximo": 10.0},
    ]


def test_media_ignora_nulos_nao_divide_por_todas_as_linhas():
    r = agregar([{"k": 1, "v": 10}, {"k": 1, "v": None}], "k", "v")
    assert r[0]["media"] == 10.0 and r[0]["linhas"] == 2


def test_zero_nao_e_nulo():
    assert agregar([{"k": "a", "v": 0}], "k", "v")[0]["soma"] == 0


def test_vazio():
    assert agregar([], "k", "v") == []
