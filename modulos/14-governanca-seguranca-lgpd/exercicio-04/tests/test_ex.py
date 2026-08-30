"""Testes do Exercício 04 (M14). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import pode_acessar  # noqa: E402


def test_pode_acessar():
    assert pode_acessar(*('analista', 'vendas', {'analista': ['vendas'], 'admin': ['vendas', 'rh']})) == True
    assert pode_acessar(*('analista', 'rh', {'analista': ['vendas'], 'admin': ['vendas', 'rh']})) == False
    assert pode_acessar(*('visita', 'vendas', {'analista': ['vendas']})) == False
