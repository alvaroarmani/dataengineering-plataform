"""Testes do Exercício 01 (M12). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import completude  # noqa: E402


def test_completude():
    assert completude(*([{'x': 1}, {'x': None}, {'x': 3}, {'y': 9}], 'x')) == 0.5
