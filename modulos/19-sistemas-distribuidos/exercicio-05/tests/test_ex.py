import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import escolher_no_de_leitura  # noqa: E402

REPLICAS = {"r1": 990, "r2": 1000, "r3": 940}


def test_menor_lag_dentro_do_limite():
    assert escolher_no_de_leitura(1000, REPLICAS, lag_max=50) == "r2"
    assert escolher_no_de_leitura(1005, REPLICAS, lag_max=50) == "r2"


def test_lag_no_limite_exato_serve():
    assert escolher_no_de_leitura(1040, {"r3": 990}, lag_max=50) == "r3"
    assert escolher_no_de_leitura(1041, {"r3": 990}, lag_max=50) == "lider"


def test_read_your_writes():
    # o cliente acabou de escrever no offset 995: r1 (990) ainda não tem a escrita
    assert escolher_no_de_leitura(1000, {"r1": 990, "r3": 940}, lag_max=100, ultima_escrita_cliente=995) == "lider"
    assert escolher_no_de_leitura(1000, REPLICAS, lag_max=100, ultima_escrita_cliente=995) == "r2"


def test_empate_e_sem_replicas():
    assert escolher_no_de_leitura(100, {"b": 90, "a": 90}, lag_max=20) == "a"
    assert escolher_no_de_leitura(100, {}, lag_max=20) == "lider"


def test_replica_a_frente_do_lider():
    with pytest.raises(ValueError):
        escolher_no_de_leitura(100, {"r1": 101}, lag_max=10)
