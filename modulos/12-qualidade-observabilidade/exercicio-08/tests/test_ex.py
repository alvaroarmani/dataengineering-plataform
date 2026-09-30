import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import faixa_iqr, pontos_anomalos  # noqa: E402


def test_faixa_basica():
    assert faixa_iqr([10, 12, 11, 13, 12, 11, 14, 12]) == (9.12, 14.12)


def test_iqr_resiste_a_um_valor_absurdo_no_historico():
    # um único 500 no histórico quase não mexe nos quartis
    assert faixa_iqr([10, 12, 11, 13, 12, 11, 14, 500]) == (7.62, 16.62)


def test_k_mais_largo():
    assert faixa_iqr([10, 12, 11, 13, 12, 11, 14, 12], k=3) == (7.25, 16.0)


def test_pontos_anomalos_com_janela_movel():
    serie = [100, 102, 98, 101, 99, 100, 180, 101, 97, 40, 100]
    assert pontos_anomalos(serie, janela=5) == [6, 8, 9]


def test_limite_e_normal():
    # faixa de [1,1,1,1] é (1.0, 1.0): o próprio 1 é normal, 1.01 não
    assert pontos_anomalos([1, 1, 1, 1, 1, 1.01], janela=4) == [5]


def test_historico_curto():
    with pytest.raises(ValueError):
        faixa_iqr([1, 2, 3])
