"""Testes do Exercicio 10 (M11). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import contar_stages  # noqa: E402


def test_contar_stages():
    assert contar_stages(*([('map', 'narrow'), ('filter', 'narrow'), ('groupBy', 'wide'), ('map', 'narrow'), ('join', 'wide')],)) == 3
    assert contar_stages(*([('map', 'narrow')],)) == 1
