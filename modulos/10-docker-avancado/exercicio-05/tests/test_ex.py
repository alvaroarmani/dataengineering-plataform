"""Testes do Exercício 05 (M10). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import resolver  # noqa: E402


def test_resolver():
    assert resolver(*('HOST:-localhost', {})) == 'localhost'
    assert resolver(*('HOST:-localhost', {'HOST': 'db'})) == 'db'
    assert resolver(*('X', {})) == ''
    assert resolver(*('HOST:-localhost', {'HOST': ''})) == 'localhost'
