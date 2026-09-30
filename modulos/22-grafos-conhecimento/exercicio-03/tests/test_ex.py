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
from solucao import ate_k_saltos, caminho_mais_curto  # noqa: E402


def test_caminho():
    assert caminho_mais_curto(REDE, "ana", "fabio") == ["ana", "bruno", "eva", "fabio"]


def test_empate_resolvido_pela_ordem_alfabetica():
    # bruno -> dara: dois caminhos de 2 saltos (via caio ou via eva); a ordem alfabética escolhe caio
    assert caminho_mais_curto(REDE, "bruno", "dara") == ["bruno", "caio", "dara"]


def test_casos_de_borda():
    assert caminho_mais_curto(REDE, "ana", "ana") == ["ana"]
    assert caminho_mais_curto(REDE, "ana", "gil") is None        # outra componente
    with pytest.raises(KeyError):
        caminho_mais_curto(REDE, "ana", "zeca")


def test_ate_k_saltos():
    assert ate_k_saltos(REDE, "ana", 1) == {"ana": 0, "bruno": 1, "caio": 1}
    assert ate_k_saltos(REDE, "ana", 2) == {"ana": 0, "bruno": 1, "caio": 1, "dara": 2, "eva": 2}
    assert ate_k_saltos(REDE, "ana", 0) == {"ana": 0}
    assert ate_k_saltos(REDE, "gil", 5) == {"gil": 0, "hugo": 1}


def test_k_negativo():
    with pytest.raises(ValueError):
        ate_k_saltos(REDE, "ana", -1)
