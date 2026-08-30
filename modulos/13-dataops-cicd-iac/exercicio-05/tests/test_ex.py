"""Testes do Exercício 05 (M13). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import plano_terraform  # noqa: E402


def test_plano_terraform():
    assert plano_terraform(*({'a': 1, 'b': 2}, {'b': 3, 'c': 4})) == {'criar': ['c'], 'atualizar': ['b'], 'destruir': ['a']}
    assert plano_terraform(*({'a': 1}, {'a': 1})) == {'criar': [], 'atualizar': [], 'destruir': []}
