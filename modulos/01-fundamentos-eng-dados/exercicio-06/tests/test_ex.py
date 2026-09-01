"""Testes do Exercicio 06 (M1). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import armazenamento_ideal  # noqa: E402


def test_armazenamento_ideal():
    assert armazenamento_ideal(*('OLTP',)) == 'linha'
    assert armazenamento_ideal(*('OLAP',)) == 'coluna'
    assert armazenamento_ideal(*('x',)) == 'indefinido'
