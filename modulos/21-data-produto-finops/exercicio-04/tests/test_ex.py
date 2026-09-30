import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import comparar, mes_de_virada, tco  # noqa: E402

SELF = {"inicial": 50_000, "mensal": 2_000, "crescimento": 0.0, "horas_mes": 40, "custo_hora": 100}
GERENCIADO = {"inicial": 0, "mensal": 7_000, "crescimento": 0.02, "horas_mes": 5, "custo_hora": 100}


def test_tco_self_hosted():
    assert tco(SELF, 12) == 122_000.0
    assert tco(SELF, 0) == 50_000.0


def test_tco_com_crescimento_composto():
    assert tco(GERENCIADO, 12) == 99_884.63
    assert tco(GERENCIADO, 36) == 381_960.57


def test_a_mais_barata_depende_do_horizonte():
    assert comparar({"self": SELF, "gerenciado": GERENCIADO}, 12)["mais_barata"] == "gerenciado"
    assert comparar({"self": SELF, "gerenciado": GERENCIADO}, 36) == {
        "tco": {"gerenciado": 381_960.57, "self": 266_000.0}, "mais_barata": "self"}


def test_mes_de_virada():
    assert mes_de_virada(SELF, GERENCIADO) == 18
    assert tco(SELF, 17) > tco(GERENCIADO, 17) and tco(SELF, 18) <= tco(GERENCIADO, 18)


def test_sem_virada_e_ja_mais_barata():
    assert mes_de_virada(SELF, GERENCIADO, max_meses=12) is None
    assert mes_de_virada(GERENCIADO, SELF) == 1


def test_meses_negativo():
    with pytest.raises(ValueError):
        tco(SELF, -1)
