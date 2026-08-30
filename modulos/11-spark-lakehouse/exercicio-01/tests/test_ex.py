"""Testes do Exercício 01 (M11). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import eh_acao  # noqa: E402


def test_eh_acao():
    assert eh_acao(*('filter',)) == False
    assert eh_acao(*('count',)) == True
    assert eh_acao(*('groupBy',)) == False
    assert eh_acao(*('write',)) == True
    assert eh_acao(*('select',)) == False
