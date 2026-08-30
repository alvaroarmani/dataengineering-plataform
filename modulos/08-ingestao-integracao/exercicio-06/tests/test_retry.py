"""Testes do Exercício 06 (M8). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import com_retry  # noqa: E402


def test_sucesso_apos_falhas():
    estado = {"n": 0}

    def instavel():
        estado["n"] += 1
        if estado["n"] < 3:
            raise RuntimeError("429 Too Many Requests")
        return "ok"

    assert com_retry(instavel, tentativas=3) == "ok"
    assert estado["n"] == 3  # falhou 2x, sucesso na 3a


def test_sucesso_de_primeira():
    assert com_retry(lambda: "pronto", tentativas=3) == "pronto"


def test_esgota_e_relanca():
    chamadas = {"n": 0}

    def sempre_falha():
        chamadas["n"] += 1
        raise RuntimeError("falha")

    with pytest.raises(RuntimeError):
        com_retry(sempre_falha, tentativas=3)
    assert chamadas["n"] == 3  # tentou exatamente 3 vezes
