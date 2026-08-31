"""Testes do Exercício 03 (M19). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import tolera_falhas  # noqa: E402


def test_tolera_falhas():
    assert tolera_falhas(*(3,)) == 1
    assert tolera_falhas(*(5,)) == 2
    assert tolera_falhas(*(1,)) == 0
