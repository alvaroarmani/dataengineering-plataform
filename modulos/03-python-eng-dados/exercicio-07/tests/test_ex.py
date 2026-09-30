import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import agrega_stream  # noqa: E402


class UmaVez:
    """Iterável que explode se alguém tentar percorrê-lo duas vezes (ou pedir len)."""
    def __init__(self, dados):
        self.dados, self.usado = dados, False

    def __iter__(self):
        if self.usado:
            raise RuntimeError("o stream só pode ser lido uma vez")
        self.usado = True
        return iter(self.dados)


def test_basico_em_uma_passada():
    r = agrega_stream(UmaVez([("a", 10), ("b", 5), ("a", 4), ("a", 7)]))
    assert r["a"] == {"n": 3, "soma": 21, "min": 4, "max": 10, "media": 7.0, "desvio": 2.4495}
    assert r["b"] == {"n": 1, "soma": 5, "min": 5, "max": 5, "media": 5.0, "desvio": 0.0}


def test_generator_de_verdade():
    gen = ((k, v) for k, v in [("x", 1), ("x", 2), ("x", 3), ("x", 4)])
    assert agrega_stream(gen)["x"]["desvio"] == 1.118


def test_valores_grandes_e_parecidos():
    base = 1_700_000_000_000                       # timestamps em ms
    r = agrega_stream(UmaVez([("t", base + d) for d in (1, 2, 3, 4)]))
    assert r["t"]["desvio"] == 1.118               # a fórmula ingênua erra aqui
    assert r["t"]["media"] == base + 2.5


def test_none_ignorado_e_vazio():
    assert agrega_stream([("a", None), ("a", 2)])["a"]["n"] == 1
    assert agrega_stream([]) == {}
