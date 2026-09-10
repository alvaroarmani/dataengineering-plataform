"""Testes do Exercicio 10 (M7). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import selecionar_incremental  # noqa: E402


def test_selecionar_incremental():
    assert selecionar_incremental(*([{'id': 1, 'updated_at': 3}, {'id': 2, 'updated_at': 7}, {'id': 3, 'updated_at': 5}], 4)) == ([{'id': 2, 'updated_at': 7}, {'id': 3, 'updated_at': 5}], 7)
    assert selecionar_incremental(*([{'id': 1, 'updated_at': 3}, {'id': 2, 'updated_at': 7}], 10)) == ([], 7)
