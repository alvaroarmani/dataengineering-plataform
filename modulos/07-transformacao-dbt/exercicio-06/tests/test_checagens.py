"""Testes do Exercício 06 (M7). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import duplicados, orfaos  # noqa: E402


def test_orfaos_encontra_violacoes():
    assert orfaos(["p1", "p2", "p9", "p1"], ["p1", "p2", "p3"]) == ["p9"]


def test_orfaos_zero_quando_integro():
    assert orfaos(["p1", "p2"], ["p1", "p2", "p3"]) == []


def test_duplicados():
    assert duplicados([1, 2, 2, 3, 3, 3]) == [2, 3]


def test_duplicados_vazio_quando_unico():
    assert duplicados([1, 2, 3]) == []
