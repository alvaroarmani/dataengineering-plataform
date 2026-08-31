"""Testes do Exercício 06 (M17). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import processar_idempotente  # noqa: E402


def test_processar_idempotente():
    assert processar_idempotente(*([(1, 10), (2, 20), (1, 10), (3, 30)],)) == 60
    assert processar_idempotente(*([(1, 5), (1, 5), (1, 5)],)) == 5
