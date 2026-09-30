import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import espera, executar_com_retry  # noqa: E402


def test_backoff_com_teto():
    assert [espera(n, 1, 30) for n in range(1, 8)] == [1, 2, 4, 8, 16, 30, 30]
    with pytest.raises(ValueError):
        espera(0, 1, 30)


def test_recupera_apos_erros_transitorios():
    r = executar_com_retry([(503, None), (502, None), (200, None)], base=1, teto=30, max_tentativas=5)
    assert r == {"resultado": "sucesso", "tentativas": 3, "esperas": [1, 2]}


def test_retry_after_manda():
    r = executar_com_retry([(429, 10), (429, 120), (200, None)], base=1, teto=60, max_tentativas=5)
    assert r == {"resultado": "sucesso", "tentativas": 3, "esperas": [10, 60]}


def test_erro_do_cliente_nao_repete():
    r = executar_com_retry([(400, None), (200, None)], base=1, teto=30, max_tentativas=5)
    assert r == {"resultado": "falha_definitiva", "tentativas": 1, "esperas": []}


def test_esgota_as_tentativas():
    r = executar_com_retry([(500, None)] * 10, base=2, teto=30, max_tentativas=4)
    assert r == {"resultado": "esgotado", "tentativas": 4, "esperas": [2, 4, 8]}
