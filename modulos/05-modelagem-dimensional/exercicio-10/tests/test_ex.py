import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import alocar_por_ponte, soma_ingenua  # noqa: E402

PONTE = {"receitas_da_vovo": {"livros": 0.5, "culinaria": 0.5},
         "panela": {"cozinha": 0.7, "culinaria": 0.3},
         "romance": {"livros": 1.0}}
FATOS = [(1, "receitas_da_vovo", 80.0), (2, "panela", 200.0), (3, "romance", 50.0), (4, "brinde", 10.0)]


def test_rateio_ponderado():
    assert alocar_por_ponte(FATOS, PONTE) == {"cozinha": 140.0, "culinaria": 100.0, "livros": 90.0,
                                              "sem_categoria": 10.0}


def test_reconciliacao():
    total = sum(r for _, _, r in FATOS)
    assert sum(alocar_por_ponte(FATOS, PONTE).values()) == pytest.approx(total)


def test_a_soma_ingenua_infla():
    assert soma_ingenua(FATOS, PONTE) == 620.0         # receita real: 340
    assert soma_ingenua([(1, "romance", 50.0)], PONTE) == 50.0


def test_pesos_invalidos():
    with pytest.raises(ValueError):
        alocar_por_ponte(FATOS, {"x": {"a": 0.5, "b": 0.4}})


def test_arredondamento_nao_quebra_a_reconciliacao():
    ponte = {"p": {"a": 1 / 3, "b": 1 / 3, "c": 1 / 3}}
    r = alocar_por_ponte([(1, "p", 100.0)], ponte)
    assert r == {"a": 33.33, "b": 33.33, "c": 33.33}
