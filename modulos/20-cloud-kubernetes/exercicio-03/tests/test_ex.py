import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import resumo, rolling_update  # noqa: E402


def test_so_surge_nunca_perde_capacidade():
    passos = rolling_update(4, max_surge=1, max_unavailable=0)
    assert passos == [(4, 1), (3, 2), (2, 3), (1, 4), (0, 4)]
    assert resumo(passos, 4) == {"passos": 5, "min_disponivel": 4, "max_total": 5}


def test_so_unavailable_nao_gasta_a_mais():
    passos = rolling_update(4, max_surge=0, max_unavailable=1)
    assert passos == [(3, 1), (2, 2), (1, 3), (0, 4)]
    assert resumo(passos, 4) == {"passos": 4, "min_disponivel": 4, "max_total": 4}


def test_folga_maior_troca_mais_rapido():
    passos = rolling_update(4, max_surge=2, max_unavailable=2)
    assert passos == [(2, 4), (0, 4)]
    assert resumo(passos, 4)["passos"] == 2


def test_recreate_na_pratica():
    passos = rolling_update(3, max_surge=0, max_unavailable=3)
    assert passos == [(0, 3)]


def test_parametros_que_travam():
    with pytest.raises(ValueError):
        rolling_update(3, 0, 0)
