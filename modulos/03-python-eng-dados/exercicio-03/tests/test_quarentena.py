"""Testes do Exercício 03 (M3). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import converter_valores  # noqa: E402


def test_basico():
    validos, invalidos = converter_valores(["10", "x", "3.5", ""])
    assert validos == [10.0, 3.5]
    assert invalidos == ["x", ""]


def test_todos_validos():
    assert converter_valores(["1", "2.5", "1e3"]) == ([1.0, 2.5, 1000.0], [])


def test_todos_invalidos():
    assert converter_valores(["a", "", ".."]) == ([], ["a", "", ".."])


def test_ordem_preservada():
    validos, invalidos = converter_valores(["5", "z", "6"])
    assert validos == [5.0, 6.0]
    assert invalidos == ["z"]


def test_lista_vazia():
    assert converter_valores([]) == ([], [])
