"""Testes do Exercício 02 (M20). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import replicas_desejadas  # noqa: E402


def test_replicas_desejadas():
    assert replicas_desejadas(*(100, 30)) == 4
    assert replicas_desejadas(*(60, 30)) == 2
    assert replicas_desejadas(*(1, 30)) == 1
