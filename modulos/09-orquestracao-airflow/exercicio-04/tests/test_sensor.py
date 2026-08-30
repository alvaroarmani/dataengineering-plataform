"""Testes do Exercício 04 (M9). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import poke_ate  # noqa: E402


def test_libera_no_terceiro_poke():
    estado = {"n": 0}

    def condicao():
        estado["n"] += 1
        return estado["n"] >= 3  # vira True no 3o poke

    assert poke_ate(condicao, max_pokes=5) == 3


def test_primeiro_poke_ja_true():
    assert poke_ate(lambda: True, max_pokes=5) == 1


def test_estoura_timeout():
    chamadas = {"n": 0}

    def nunca():
        chamadas["n"] += 1
        return False

    with pytest.raises(TimeoutError):
        poke_ate(nunca, max_pokes=4)
    assert chamadas["n"] == 4  # pokou exatamente o limite
