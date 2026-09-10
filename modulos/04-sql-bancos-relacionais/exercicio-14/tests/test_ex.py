"""Testes do Exercicio 14 (M4). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import particoes_varridas  # noqa: E402


def test_particoes_varridas():
    assert particoes_varridas(*([(1, 10), (11, 20), (21, 30)], 5, 15)) == 2
    assert particoes_varridas(*([(1, 10), (11, 20)], 25, 30)) == 0
    assert particoes_varridas(*([(1, 10)], 1, 10)) == 1
