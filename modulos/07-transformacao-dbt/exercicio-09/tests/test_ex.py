"""Testes do Exercicio 09 (M7). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import merge_incremental  # noqa: E402


def test_merge_incremental():
    assert merge_incremental(*([{'id': 1, 'valor': 10, 'updated_at': 5}, {'id': 2, 'valor': 20, 'updated_at': 5}], [{'id': 2, 'valor': 99, 'updated_at': 8}, {'id': 3, 'valor': 30, 'updated_at': 7}, {'id': 1, 'valor': 1, 'updated_at': 2}], 'id')) == [{'id': 1, 'valor': 10, 'updated_at': 5}, {'id': 2, 'valor': 99, 'updated_at': 8}, {'id': 3, 'valor': 30, 'updated_at': 7}]
    assert merge_incremental(*([{'id': 1, 'valor': 10, 'updated_at': 5}], [{'id': 2, 'valor': 20, 'updated_at': 1}], 'id')) == [{'id': 1, 'valor': 10, 'updated_at': 5}, {'id': 2, 'valor': 20, 'updated_at': 1}]
