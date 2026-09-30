import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import avaliar_investimento  # noqa: E402


def test_projeto_em_12_meses():
    assert avaliar_investimento(120_000, 30_000, 10_000, 12) == {
        "roi": 0.5, "payback_mes": 6, "resultado": 120_000}


def test_mesmo_projeto_em_4_meses():
    assert avaliar_investimento(120_000, 30_000, 10_000, 4) == {
        "roi": -0.25, "payback_mes": None, "resultado": -40_000}


def test_projeto_que_nunca_se_paga():
    r = avaliar_investimento(120_000, 10_000, 12_000, 24)
    assert r == {"roi": -0.4118, "payback_mes": None, "resultado": -168_000}


def test_payback_no_limite_exato():
    assert avaliar_investimento(100, 60, 10, 2)["payback_mes"] == 2     # 50*2 == 100


def test_sem_investimento_inicial():
    assert avaliar_investimento(0, 50, 10, 3) == {"roi": 4.0, "payback_mes": 1, "resultado": 120}


@pytest.mark.parametrize("args", [(-1, 10, 1, 12), (100, 10, 1, 0), (100, -5, 1, 12)])
def test_parametros_invalidos(args):
    with pytest.raises(ValueError):
        avaliar_investimento(*args)
