"""Testes do Exercício 06 (M19). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import menor_carga  # noqa: E402


def test_menor_carga():
    assert menor_carga(*({'a': 5, 'b': 3, 'c': 3},)) == 'b'
    assert menor_carga(*({'x': 1},)) == 'x'
