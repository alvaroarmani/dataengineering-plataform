"""Testes do Exercicio 11 (M11). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import particoes_com_skew  # noqa: E402


def test_particoes_com_skew():
    assert particoes_com_skew(*([10, 10, 10, 100], 2.0)) == [3]
    assert particoes_com_skew(*([10, 10], 2.0)) == []
