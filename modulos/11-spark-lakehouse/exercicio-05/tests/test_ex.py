"""Testes do Exercício 05 (M11). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import causa_shuffle  # noqa: E402


def test_causa_shuffle():
    assert causa_shuffle(*('filter',)) == False
    assert causa_shuffle(*('groupBy',)) == True
    assert causa_shuffle(*('join',)) == True
    assert causa_shuffle(*('select',)) == False
    assert causa_shuffle(*('orderBy',)) == True
