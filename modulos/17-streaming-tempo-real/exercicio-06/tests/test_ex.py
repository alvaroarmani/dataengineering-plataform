import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import processar  # noqa: E402

LOG = [("m1", 10), ("m2", 20), ("m3", 30), ("m4", 40), ("m5", 50)]


def _inicio():
    return {"offset": 0, "saldo": 0, "aplicados": set()}


def test_sem_falha():
    r = processar(LOG, _inicio(), commit_a_cada=2)
    assert r == {"offset": 5, "saldo": 150, "aplicados": {"m1", "m2", "m3", "m4", "m5"}}


def test_falha_antes_do_commit():
    caiu = processar(LOG, _inicio(), commit_a_cada=2, falha_apos=3)
    assert caiu["offset"] == 2 and caiu["saldo"] == 60     # m3 aplicado, mas não commitado


def test_reprocessamento_sem_idempotencia_duplica():
    caiu = processar(LOG, _inicio(), commit_a_cada=2, falha_apos=3, idempotente=False)
    final = processar(LOG, caiu, commit_a_cada=2, idempotente=False)
    assert final["saldo"] == 180                           # m3 creditado duas vezes


def test_reprocessamento_idempotente_fica_correto():
    caiu = processar(LOG, _inicio(), commit_a_cada=2, falha_apos=3)
    final = processar(LOG, caiu, commit_a_cada=2)
    assert final == {"offset": 5, "saldo": 150, "aplicados": {"m1", "m2", "m3", "m4", "m5"}}


def test_reentrega_do_broker_tambem_e_absorvida():
    log = LOG + [("m2", 20)]                               # o produtor reenviou m2
    assert processar(log, _inicio(), commit_a_cada=10)["saldo"] == 150


def test_nao_altera_entrada():
    ini = _inicio()
    processar(LOG, ini, commit_a_cada=1)
    assert ini == _inicio()
