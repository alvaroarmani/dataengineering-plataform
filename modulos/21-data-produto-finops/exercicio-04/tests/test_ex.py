"""Testes do Exercício 04 (M21). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import tco  # noqa: E402


def test_tco():
    assert tco(*(1000, 200, 12)) == 3400
    assert tco(*(0, 50, 6)) == 300
