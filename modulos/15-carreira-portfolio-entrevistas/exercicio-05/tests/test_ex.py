"""Testes do Exercício 05 (M15). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import escolher_processamento  # noqa: E402


def test_escolher_processamento():
    assert escolher_processamento(*(5,)) == 'streaming'
    assert escolher_processamento(*(3600,)) == 'batch'
    assert escolher_processamento(*(60,)) == 'batch'
