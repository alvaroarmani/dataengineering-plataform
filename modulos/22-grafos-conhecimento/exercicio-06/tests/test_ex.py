"""Testes do Exercicio 06 (M22). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import componente  # noqa: E402


def test_componente():
    assert componente(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']}, 'ana')) == ['ana', 'bruno', 'caio', 'dara']
    assert componente(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']}, 'elo')) == ['elo', 'formiga']
