"""Testes do Exercicio 05 (M22). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import mais_conectado  # noqa: E402


def test_mais_conectado():
    assert mais_conectado(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']},)) == 'caio'
