"""Testes do Exercício 07 (M9). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import executar_com_retries  # noqa: E402


def _falha_ate(k):
    estado = {"n": 0}

    def fn():
        estado["n"] += 1
        if estado["n"] < k:
            raise RuntimeError("falha transitória")
        return "ok"

    return fn


def test_sucesso_de_primeira():
    assert executar_com_retries(lambda: "ok", retries=2) == (True, 1)


def test_sucesso_apos_retries():
    # passa na 3a tentativa; retries=2 permite exatamente 3
    assert executar_com_retries(_falha_ate(3), retries=2) == (True, 3)


def test_falha_apos_todas():
    chamadas = {"n": 0}

    def sempre_falha():
        chamadas["n"] += 1
        raise RuntimeError("falha")

    assert executar_com_retries(sempre_falha, retries=2) == (False, 3)
    assert chamadas["n"] == 3  # 1 + 2 retries
