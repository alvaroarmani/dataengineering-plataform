"""Testes do Exercicio 04 (M23). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import backoff  # noqa: E402


def test_backoff():
    assert backoff(*(1, 1)) == 1
    assert backoff(*(3, 1)) == 4
    assert backoff(*(4, 2)) == 16
