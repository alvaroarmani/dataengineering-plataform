"""Testes do Exercicio 03 (M22). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import distancia_em_saltos  # noqa: E402


def test_distancia_em_saltos():
    assert distancia_em_saltos(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']}, 'ana', 'dara')) == 2
    assert distancia_em_saltos(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']}, 'ana', 'ana')) == 0
    assert distancia_em_saltos(*({'ana': ['bruno', 'caio'], 'bruno': ['ana', 'caio'], 'caio': ['ana', 'bruno', 'dara'], 'dara': ['caio'], 'elo': ['formiga'], 'formiga': ['elo']}, 'ana', 'elo')) == -1
