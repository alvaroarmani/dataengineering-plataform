import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import Cache  # noqa: E402


def test_ttl_expira_na_leitura():
    c = Cache(10)
    c.set("sessao:1", "ana", agora=0, ttl=30)
    assert c.get("sessao:1", agora=29) == "ana"
    assert c.get("sessao:1", agora=30) is None          # agora >= gravada + ttl
    assert (c.hits, c.misses, c.expiradas) == (1, 1, 1)


def test_sem_ttl_nao_expira():
    c = Cache(2)
    c.set("cfg", {"tema": "escuro"}, agora=0)
    assert c.get("cfg", agora=10**9) == {"tema": "escuro"}


def test_lru_despeja_o_menos_usado():
    c = Cache(2)
    c.set("a", 1, agora=0)
    c.set("b", 2, agora=1)
    c.get("a", agora=2)                 # "a" vira a mais recente
    c.set("c", 3, agora=3)              # cheio: despeja "b"
    assert c.get("b", agora=4) is None
    assert c.get("a", agora=4) == 1 and c.get("c", agora=4) == 3
    assert c.despejos == 1


def test_vencidas_saem_antes_de_despejar_as_validas():
    c = Cache(2)
    c.set("temp", "x", agora=0, ttl=5)
    c.set("fixa", "y", agora=1)
    c.set("nova", "z", agora=10)        # "temp" já venceu: sai ela, não a LRU válida
    assert (c.expiradas, c.despejos) == (1, 0)
    assert c.get("fixa", agora=11) == "y"


def test_sobrescrever_nao_despeja_e_renova_ttl():
    c = Cache(1)
    c.set("k", 1, agora=0, ttl=10)
    c.set("k", 2, agora=8, ttl=10)
    assert c.get("k", agora=15) == 2 and c.despejos == 0


def test_hit_rate_e_capacidade_invalida():
    c = Cache(3)
    assert c.hit_rate() == 0.0
    c.set("x", 1, agora=0)
    for _ in range(3):
        c.get("x", agora=1)
    c.get("y", agora=1)
    assert c.hit_rate() == 0.75
    with pytest.raises(ValueError):
        Cache(0)
