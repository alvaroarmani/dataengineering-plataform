"""Testes do Exercicio 10 (M9). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import tarefas_prontas  # noqa: E402


def test_tarefas_prontas():
    assert tarefas_prontas(*({'a': [], 'b': ['a'], 'c': ['a'], 'd': ['b', 'c']}, ['a'])) == ['b', 'c']
    assert tarefas_prontas(*({'a': [], 'b': ['a'], 'c': ['a'], 'd': ['b', 'c']}, [])) == ['a']
