import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import simular_pool  # noqa: E402

ARQUIVOS = [10, 3, 3, 3, 25, 3, 3, 10]       # minutos por arquivo, na ordem da listagem


def test_pool_de_2():
    assert simular_pool(ARQUIVOS, 2) == {"inicio": [0, 0, 3, 6, 9, 10, 13, 16], "total": 34}


def test_mais_slots_menos_tempo():
    assert simular_pool(ARQUIVOS, 4)["total"] == 28
    assert simular_pool(ARQUIVOS, 8)["total"] == 25       # limitado pelo arquivo mais longo


def test_maiores_primeiro_reduz_o_total():
    assert simular_pool(ARQUIVOS, 2, maiores_primeiro=True) == {
        "inicio": [0, 20, 23, 25, 0, 26, 28, 10], "total": 31}


def test_um_slot_e_serial():
    assert simular_pool([5, 5, 5], 1) == {"inicio": [0, 5, 10], "total": 15}


def test_vazio_e_invalido():
    assert simular_pool([], 3) == {"inicio": [], "total": 0}
    with pytest.raises(ValueError):
        simular_pool([1], 0)
