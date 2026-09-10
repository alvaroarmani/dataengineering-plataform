"""Testes do Exercicio 04 (M22). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import amigos_em_comum  # noqa: E402


def test_amigos_em_comum():
    assert amigos_em_comum(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']}, 'ana', 'bruno')) == ['caio']
    assert amigos_em_comum(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']}, 'ana', 'dara')) == ['caio']
