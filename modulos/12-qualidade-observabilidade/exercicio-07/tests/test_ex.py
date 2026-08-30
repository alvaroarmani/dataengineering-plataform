"""Testes do Exercício 07 (M12). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import deve_alertar  # noqa: E402


def test_deve_alertar():
    assert deve_alertar(*([('a', 'pass'), ('b', 'fail')],)) == True
    assert deve_alertar(*([('a', 'pass'), ('b', 'warn')],)) == False
