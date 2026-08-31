"""Testes do Exercício 05 (M21). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import cumpre_sla  # noqa: E402


def test_cumpre_sla():
    assert cumpre_sla(*(99.95, 99.9)) == True
    assert cumpre_sla(*(99.5, 99.9)) == False
    assert cumpre_sla(*(99.9, 99.9)) == True
