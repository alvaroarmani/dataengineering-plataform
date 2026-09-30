import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import tratar  # noqa: E402


def _armazem():
    return {"chaves": {}, "proximo_id": 1, "cobrancas": []}


def test_retry_nao_cobra_duas_vezes():
    a = _armazem()
    corpo = {"cliente": "ana", "valor": 99.9}
    assert tratar(a, "k-1", corpo, agora=0) == (201, {"id": 1, "cliente": "ana", "valor": 99.9}, False)
    assert tratar(a, "k-1", dict(corpo), agora=5) == (200, {"id": 1, "cliente": "ana", "valor": 99.9}, True)
    assert len(a["cobrancas"]) == 1


def test_ordem_das_chaves_do_corpo_nao_importa():
    a = _armazem()
    tratar(a, "k-1", {"cliente": "ana", "valor": 10}, agora=0)
    assert tratar(a, "k-1", {"valor": 10, "cliente": "ana"}, agora=1)[0] == 200


def test_mesma_chave_outro_corpo_e_erro():
    a = _armazem()
    tratar(a, "k-1", {"cliente": "ana", "valor": 10}, agora=0)
    status, resp, replay = tratar(a, "k-1", {"cliente": "ana", "valor": 1000}, agora=1)
    assert status == 422 and "erro" in resp and replay is False
    assert len(a["cobrancas"]) == 1


def test_chaves_diferentes_sao_operacoes_diferentes():
    a = _armazem()
    tratar(a, "k-1", {"valor": 10}, agora=0)
    assert tratar(a, "k-2", {"valor": 10}, agora=0)[1]["id"] == 2


def test_chave_expirada_executa_de_novo():
    a = _armazem()
    tratar(a, "k-1", {"valor": 10}, agora=0, ttl_seg=60)
    assert tratar(a, "k-1", {"valor": 10}, agora=59, ttl_seg=60)[2] is True
    assert tratar(a, "k-1", {"valor": 10}, agora=60, ttl_seg=60)[0] == 201
    with pytest.raises(ValueError):
        tratar(a, "", {"valor": 10}, agora=0)
