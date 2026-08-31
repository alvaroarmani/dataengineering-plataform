"""Testes do Exercício 04 (M19). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import tem_consenso  # noqa: E402


def test_tem_consenso():
    assert tem_consenso(*(3, 5)) == True
    assert tem_consenso(*(2, 5)) == False
    assert tem_consenso(*(2, 4)) == False
