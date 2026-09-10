"""Testes do Exercicio 01 (M22). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import vizinhos  # noqa: E402


def test_vizinhos():
    assert vizinhos(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']}, 'caio')) == ['ana', 'bruno', 'dara']
    assert vizinhos(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']}, 'dara')) == ['caio']
