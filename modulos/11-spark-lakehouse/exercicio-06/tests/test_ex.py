"""Testes do Exercício 06 (M11). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import n_shuffles  # noqa: E402


def test_n_shuffles():
    assert n_shuffles(*(['filter', 'groupBy', 'select', 'join'],)) == 2
    assert n_shuffles(*(['filter', 'select'],)) == 0
    assert n_shuffles(*(['distinct'],)) == 1
