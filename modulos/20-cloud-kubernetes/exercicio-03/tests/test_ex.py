"""Testes do Exercício 03 (M20). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import deployment_saudavel  # noqa: E402


def test_deployment_saudavel():
    assert deployment_saudavel(*(3, 3)) == True
    assert deployment_saudavel(*(3, 2)) == False
    assert deployment_saudavel(*(3, 4)) == True
