"""Testes do Exercício 02 (M17). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import classifica_latencia  # noqa: E402


def test_classifica_latencia():
    assert classifica_latencia(*(0.2,)) == 'tempo-real'
    assert classifica_latencia(*(5,)) == 'quase-real'
    assert classifica_latencia(*(3600,)) == 'batch'
