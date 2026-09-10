"""Testes do Exercicio 07 (M18). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import indice_invertido  # noqa: E402


def test_indice_invertido():
    assert indice_invertido(*([(1, 'gato preto'), (2, 'gato branco')],)) == {'gato': [1, 2], 'preto': [1], 'branco': [2]}
    assert indice_invertido(*([(1, 'sol')],)) == {'sol': [1]}
