"""Testes do Exercicio 02 (M23). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import paginar  # noqa: E402


def test_paginar():
    assert paginar(*([1, 2, 3, 4, 5], 1, 2)) == [1, 2]
    assert paginar(*([1, 2, 3, 4, 5], 3, 2)) == [5]
    assert paginar(*([1, 2], 5, 2)) == []
