"""Testes do Exercício 06 (M13). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import num_mudancas  # noqa: E402


def test_num_mudancas():
    assert num_mudancas(*({'a': 1, 'b': 2}, {'b': 3, 'c': 4})) == 3
    assert num_mudancas(*({'a': 1}, {'a': 1})) == 0
