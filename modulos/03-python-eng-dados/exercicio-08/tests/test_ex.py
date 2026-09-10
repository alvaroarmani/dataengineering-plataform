"""Testes do Exercicio 08 (M3). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import sessionizar  # noqa: E402


def test_sessionizar():
    assert sessionizar(*([('a', 1), ('a', 2), ('a', 10), ('b', 5)], 3)) == {'a': [2, 1], 'b': [1]}
    assert sessionizar(*([('a', 1)], 3)) == {'a': [1]}
