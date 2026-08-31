"""Testes do Exercício 03 (M18). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import expirou  # noqa: E402


def test_expirou():
    assert expirou(*(100, 50, 30)) == True
    assert expirou(*(100, 90, 30)) == False
    assert expirou(*(130, 100, 30)) == True
