"""Testes do Exercício 01 (M13). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import pode_mergear  # noqa: E402


def test_pode_mergear():
    assert pode_mergear(*([('lint', 'pass'), ('test', 'pass')],)) == True
    assert pode_mergear(*([('lint', 'pass'), ('test', 'fail')],)) == False
