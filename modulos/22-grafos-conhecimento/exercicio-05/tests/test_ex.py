import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

REDE = {
    "ana": ["bruno", "caio"],
    "bruno": ["ana", "caio", "eva"],
    "caio": ["ana", "bruno", "dara"],
    "dara": ["caio", "eva"],
    "eva": ["bruno", "dara", "fabio"],
    "fabio": ["eva"],
    "gil": ["hugo"],
    "hugo": ["gil"],
}
from solucao import ranking_centralidade  # noqa: E402


def test_ranking():
    assert ranking_centralidade(REDE) == [
        ("bruno", 3, 0.429, 5),
        ("eva", 3, 0.429, 5),
        ("caio", 3, 0.429, 4),
    ]


def test_alcance_desempata_o_grau():
    completo = ranking_centralidade(REDE, top_n=8)
    assert [x[0] for x in completo] == ["bruno", "eva", "caio", "dara", "ana", "fabio", "gil", "hugo"]
    assert completo[-2:] == [("gil", 1, 0.143, 1), ("hugo", 1, 0.143, 1)]


def test_rede_minima():
    assert ranking_centralidade({"x": []}) == [("x", 0, 0.0, 0)]


def test_vazio():
    with pytest.raises(ValueError):
        ranking_centralidade({})
