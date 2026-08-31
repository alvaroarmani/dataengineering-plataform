"""Testes do Exercício 06 (M18). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import leitura_consistente  # noqa: E402


def test_leitura_consistente():
    assert leitura_consistente(*(3, 2, 2)) == True
    assert leitura_consistente(*(3, 1, 1)) == False
    assert leitura_consistente(*(3, 3, 1)) == True
