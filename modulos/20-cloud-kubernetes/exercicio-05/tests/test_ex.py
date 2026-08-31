"""Testes do Exercício 05 (M20). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import cabe_no_no  # noqa: E402


def test_cabe_no_no():
    assert cabe_no_no(*([2, 2, 3], 8)) == True
    assert cabe_no_no(*([4, 4, 4], 8)) == False
    assert cabe_no_no(*([], 8)) == True
