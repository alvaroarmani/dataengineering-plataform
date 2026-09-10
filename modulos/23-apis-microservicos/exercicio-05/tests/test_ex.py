"""Testes do Exercicio 05 (M23). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import compensacoes  # noqa: E402


def test_compensacoes():
    assert compensacoes(*(['reservar', 'cobrar'],)) == ['estornar', 'liberar']
    assert compensacoes(*(['reservar'],)) == ['liberar']
