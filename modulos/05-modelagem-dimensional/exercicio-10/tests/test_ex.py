"""Testes do Exercicio 10 (M5). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import alocar_por_ponte  # noqa: E402


def test_alocar_por_ponte():
    assert alocar_por_ponte(*([(1, 'A', 100.0), (2, 'B', 50.0)], {'A': {'livros': 0.5, 'papelaria': 0.5}, 'B': {'livros': 1.0}})) == {'livros': 100.0, 'papelaria': 50.0}
    assert alocar_por_ponte(*([(1, 'A', 30.0)], {'A': {'x': 1.0}})) == {'x': 30.0}
