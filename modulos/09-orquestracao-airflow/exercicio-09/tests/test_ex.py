"""Testes do Exercicio 09 (M9). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import ordem_topologica  # noqa: E402


def test_ordem_topologica():
    assert ordem_topologica(*({'a': [], 'b': ['a'], 'c': ['a'], 'd': ['b', 'c']},)) == ['a', 'b', 'c', 'd']
    assert ordem_topologica(*({'a': ['b'], 'b': ['a']},)) == None
