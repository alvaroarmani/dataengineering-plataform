"""Testes do Exercício 01 (M14). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import impactados  # noqa: E402


def test_impactados():
    assert impactados(*({'a': ['b', 'c'], 'b': ['d'], 'c': [], 'd': []}, 'a')) == ['b', 'c', 'd']
    assert impactados(*({'a': ['b', 'c'], 'b': ['d'], 'c': [], 'd': []}, 'b')) == ['d']
    assert impactados(*({'a': ['b'], 'b': []}, 'b')) == []
