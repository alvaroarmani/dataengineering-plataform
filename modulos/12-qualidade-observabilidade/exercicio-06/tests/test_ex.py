import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import avaliar_volume  # noqa: E402

ESTAVEL = [1000, 1010, 990, 1005, 995, 1000, 1000]          # média 1000, desvio ~5,9
VOLATIL = [800, 1200, 900, 1100, 1000, 700, 1300]            # média 1000, desvio 200


def test_queda_de_5pct_em_tabela_estavel_e_anomalia():
    assert avaliar_volume(ESTAVEL, 950) == {"anomalia": True, "z": -8.37, "direcao": "queda"}


def test_mesma_queda_em_tabela_volatil_e_normal():
    assert avaliar_volume(VOLATIL, 950) == {"anomalia": False, "z": -0.25, "direcao": None}


def test_alta_na_tabela_volatil():
    assert avaliar_volume(VOLATIL, 1700) == {"anomalia": True, "z": 3.5, "direcao": "alta"}


def test_limite_exato_nao_e_anomalia():
    assert avaliar_volume(VOLATIL, 1600)["anomalia"] is False       # z = 3.0, não > 3.0
    assert avaliar_volume(VOLATIL, 1600, z_max=2.5)["anomalia"] is True


def test_historico_constante():
    assert avaliar_volume([500] * 7, 500) == {"anomalia": False, "z": None, "direcao": None}
    assert avaliar_volume([500] * 7, 0) == {"anomalia": True, "z": None, "direcao": "queda"}


def test_historico_curto():
    with pytest.raises(ValueError):
        avaliar_volume([100, 100, 100], 100)
    assert avaliar_volume([100, 100, 100], 100, min_historico=3)["anomalia"] is False
