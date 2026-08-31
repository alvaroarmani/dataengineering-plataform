"""Testes do Exercício 03 (M21). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import roi  # noqa: E402


def test_roi():
    assert roi(*(300, 100)) == 2.0
    assert roi(*(150, 100)) == 0.5
