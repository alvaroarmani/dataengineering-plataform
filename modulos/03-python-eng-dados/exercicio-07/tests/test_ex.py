"""Testes do Exercicio 07 (M3). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import agrega_stream  # noqa: E402


def test_agrega_stream():
    assert agrega_stream(*([('a', 10), ('b', 5), ('a', 3)],)) == {'a': (2, 13, 10), 'b': (1, 5, 5)}
    assert agrega_stream(*([('x', 7)],)) == {'x': (1, 7, 7)}
