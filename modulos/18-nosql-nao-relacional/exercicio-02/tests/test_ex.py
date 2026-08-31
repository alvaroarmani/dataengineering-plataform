"""Testes do Exercício 02 (M18). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import contar_por  # noqa: E402


def test_contar_por():
    assert contar_por(*([{'cat': 'a'}, {'cat': 'b'}, {'cat': 'a'}], 'cat')) == {'a': 2, 'b': 1}
    assert contar_por(*([{'x': 1}], 'x')) == {1: 1}
