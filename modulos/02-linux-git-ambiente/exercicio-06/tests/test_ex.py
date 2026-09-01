"""Testes do Exercicio 06 (M2). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import mapa_porta  # noqa: E402


def test_mapa_porta():
    assert mapa_porta(*(8080, 80)) == '8080:80'
    assert mapa_porta(*(5432, 5432)) == '5432:5432'
