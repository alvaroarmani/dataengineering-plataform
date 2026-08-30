"""Testes do Exercício 04 (M13). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import deve_deployar  # noqa: E402


def test_deve_deployar():
    assert deve_deployar(*('main', True)) == True
    assert deve_deployar(*('main', False)) == False
    assert deve_deployar(*('feature/x', True)) == False
