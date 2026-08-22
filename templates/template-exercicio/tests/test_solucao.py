"""Suíte de testes do exercício. O aluno faz tudo ficar verde.

Executar: pytest -q  (a partir da pasta do exercício)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import resolver  # noqa: E402


def test_exemplo_basico():
    assert resolver([2, 4]) == 3


def test_caso_borda():
    # Defina o comportamento esperado para entradas de borda.
    assert resolver([10]) == 10
