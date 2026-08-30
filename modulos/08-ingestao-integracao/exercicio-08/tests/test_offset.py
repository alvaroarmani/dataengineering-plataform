"""Testes do Exercício 08 (M8). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import consumir  # noqa: E402

LOG = ["m0", "m1", "m2", "m3"]


def test_consome_do_offset():
    assert consumir(LOG, 2) == (["m2", "m3"], 4)


def test_consome_tudo_do_zero():
    assert consumir(LOG, 0) == (["m0", "m1", "m2", "m3"], 4)


def test_nada_novo():
    # offset no fim: nenhuma mensagem nova, offset não muda
    assert consumir(LOG, 4) == ([], 4)
