import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import falhas_toleradas, lado_com_quorum, nos_para_tolerar  # noqa: E402


@pytest.mark.parametrize("n, f", [(1, 0), (2, 0), (3, 1), (4, 1), (5, 2), (6, 2), (7, 3)])
def test_falhas_toleradas(n, f):
    assert falhas_toleradas(n) == f


def test_par_nao_compra_tolerancia():
    assert falhas_toleradas(4) == falhas_toleradas(3)
    assert nos_para_tolerar(2) == 5


def test_particao_com_maioria():
    assert lado_com_quorum(5, [{"a", "b", "c"}, {"d", "e"}]) == 0
    assert lado_com_quorum(5, [{"a"}, {"b", "c", "d", "e"}]) == 1


def test_empate_em_cluster_par_ninguem_continua():
    assert lado_com_quorum(4, [{"a", "b"}, {"c", "d"}]) is None


def test_nos_mortos_contam_contra():
    # 5 nós, 2 morreram, os 3 vivos se partiram em 2 + 1: ninguém tem 3 de 5
    assert lado_com_quorum(5, [{"a", "b"}, {"c"}]) is None
    assert lado_com_quorum(5, [{"a", "b", "c"}]) == 0


def test_entradas_invalidas():
    with pytest.raises(ValueError):
        lado_com_quorum(3, [{"a", "b"}, {"b", "c"}])
    with pytest.raises(ValueError):
        falhas_toleradas(0)
