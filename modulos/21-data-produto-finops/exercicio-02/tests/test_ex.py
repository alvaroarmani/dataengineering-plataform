"""Testes do Exercício 02 (M21). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import economia_particao  # noqa: E402


def test_economia_particao():
    assert economia_particao(*(10, 0.1, 5.0)) == 45.0
    assert economia_particao(*(4, 1.0, 5.0)) == 0.0
