"""Testes do Exercício 05 (M18). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import downsample_soma  # noqa: E402


def test_downsample_soma():
    assert downsample_soma(*([(0, 1), (30, 2), (60, 3), (90, 4)], 60)) == {0: 3, 60: 7}
    assert downsample_soma(*([(5, 10)], 60)) == {0: 10}
