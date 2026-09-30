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
from solucao import amigos_em_comum, recomendar  # noqa: E402


def test_amigos_em_comum():
    assert amigos_em_comum(REDE, "ana", "bruno") == ["caio"]
    assert amigos_em_comum(REDE, "bruno", "dara") == ["caio", "eva"]
    assert amigos_em_comum(REDE, "ana", "gil") == []


def test_recomendar_ordena_por_amigos_em_comum():
    assert recomendar(REDE, "ana") == [("dara", 1), ("eva", 1)]
    assert recomendar(REDE, "dara") == [("bruno", 2), ("ana", 1), ("fabio", 1)]


def test_nao_recomenda_quem_ja_e_amigo_nem_a_si_mesmo():
    nomes = [n for n, _ in recomendar(REDE, "bruno", top_n=10)]
    assert "bruno" not in nomes and not set(nomes) & set(REDE["bruno"])
    assert nomes == ["dara", "fabio"]


def test_top_n_e_isolados():
    assert recomendar(REDE, "dara", top_n=1) == [("bruno", 2)]
    assert recomendar(REDE, "gil") == []


def test_pessoa_inexistente():
    with pytest.raises(KeyError):
        recomendar(REDE, "zeca")
