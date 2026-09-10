"""Testes do Exercicio 08 (M18). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import ranquear  # noqa: E402


def test_ranquear():
    assert ranquear(*([(1, 'gato gato cao'), (2, 'gato'), (3, 'cao')], 'gato')) == [1, 2]
    assert ranquear(*([(1, 'gato gato cao'), (2, 'gato'), (3, 'cao')], 'cao')) == [1, 3]
