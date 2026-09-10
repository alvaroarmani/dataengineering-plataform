"""Testes do Exercicio 09 (M6). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import bytes_varridos  # noqa: E402


def test_bytes_varridos():
    assert bytes_varridos(*({'a': 100, 'b': 200, 'c': 100}, ['a', 'c'], 10, 2)) == 40.0
    assert bytes_varridos(*({'a': 50}, ['a'], 4, 4)) == 50.0
