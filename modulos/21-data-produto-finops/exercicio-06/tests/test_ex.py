"""Testes do Exercício 06 (M21). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import requisitos_faltando  # noqa: E402


def test_requisitos_faltando():
    assert requisitos_faltando(*({'dono': True, 'sla': False, 'doc': True, 'qualidade': False},)) == ['qualidade', 'sla']
    assert requisitos_faltando(*({'dono': True, 'sla': True, 'doc': True, 'qualidade': True},)) == []
