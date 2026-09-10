"""Testes do Exercicio 10 (M8). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import conciliar_schema  # noqa: E402


def test_conciliar_schema():
    assert conciliar_schema(*({'id': 'int', 'nome': 'str'}, {'id': 1, 'extra': 9})) == {'faltando': ['nome'], 'extras': ['extra'], 'tipo_incompativel': []}
    assert conciliar_schema(*({'id': 'int'}, {'id': 'abc'})) == {'faltando': [], 'extras': [], 'tipo_incompativel': ['id']}
